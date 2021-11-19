import pickle
from fmi2 import Fmi2FMU, Fmi2Status
from control import ss
from filterpy.common import Q_discrete_white_noise
from filterpy.kalman import KalmanFilter
import sympy as sp
import numpy as np

HEATER_VOLTAGE = 12.0
HEATER_CURRENT = 10.45
STEP_SIZE = 3.0

class Model(Fmi2FMU):
    def __init__(self, reference_to_attr=None) -> None:
        super().__init__(reference_to_attr)
        self.T_room_in = 0.0
        self.T_bair_in = -1.0
        self.heater_on_in = False
        self.T_heater_out = 0.0
        self.T_bair_out = -1.0
        self.G_heater = 30.0
        self.C_heater = 30.0
        self.filter = None
        self.state = "Instantiated"

    def enter_initialization_mode(self) -> int:
        self.state = "Initializing"
        return Fmi2Status.ok

    def exit_initialization_mode(self):
        """Informs the fmu to exit initialization mode."""
        self.filter = self.construct_filter(step_size = STEP_SIZE, 
                                            std_dev = 0.00001, 
                                            C_air_num = 68.20829072, 
                                            G_box_num = 0.73572788, 
                                            C_heater_num = 243.45802367, 
                                            G_heater_num = 0.87095429, 
                                            initial_heat_temperature = self.T_bair_in, 
                                            initial_box_temperature = self.T_bair_in)
        self.state = "Stepping"
        return Fmi2Status.ok
    
    def get_xxx(self, references):
        if self.state == "Initializing":
            # Implement feedthrough during initialization mode
            # assert self.T_bair_in >= 0.0
            self.T_bair_out = self.T_bair_in
        
        return super().get_xxx(references)

    def do_step(self, current_time, step_size, no_step_prior):
        assert np.isclose(step_size, STEP_SIZE)

        assert self.filter is not None
        
        self.filter.predict(u=np.array([
            [1.0 if self.heater_on_in else 0.0],
            [self.T_room_in]
        ]))
        self.filter.update(np.array([[self.T_bair_in]]))
        
        self.T_heater_out = self.filter.x[0, 0]
        self.T_bair_out = self.filter.x[1, 0]

        return Fmi2Status.ok

    def construct_filter(self, 
                     step_size, std_dev,
                     C_air_num,
                     G_box_num,
                     C_heater_num,
                     G_heater_num,
                     initial_heat_temperature,
                     initial_box_temperature):
        # Parameters
        C_air = sp.symbols("C_air")  # Specific heat capacity
        G_box = sp.symbols("G_box")  # Specific heat capacity
        C_heater = sp.symbols("C_heater")  # Specific heat capacity
        G_heater = sp.symbols("G_heater")  # Specific heat capacity

        # Constants
        V_heater = sp.symbols("V_heater")
        i_heater = sp.symbols("i_heater")

        # Inputs
        in_room_temperature = sp.symbols("T_room")
        on_heater = sp.symbols("on_heater")

        # States
        T = sp.symbols("T")
        T_heater = sp.symbols("T_h")

        power_in = on_heater * V_heater * i_heater

        power_transfer_heat = G_heater * (T_heater - T)

        total_power_heater = power_in - power_transfer_heat

        power_out_box = G_box * (T - in_room_temperature)

        total_power_box = power_transfer_heat - power_out_box

        der_T = (1.0 / C_air) * (total_power_box)
        der_T_heater = (1.0 / C_heater) * (total_power_heater)

        # Turn above into a CT linear system
        """
        States are:
        [[ T_heater ]
        [ T        ]]

        Inputs are: 
        [ [ on_heater ], 
        [ in_room_ptemperature ]]
        """
        A = sp.Matrix([
            [der_T_heater.diff(T_heater), der_T_heater.diff(T)],
            [der_T.diff(T_heater), der_T.diff(T)]
        ])

        B = sp.Matrix([
            [der_T_heater.diff(on_heater), der_T_heater.diff(in_room_temperature)],
            [der_T.diff(on_heater), der_T.diff(in_room_temperature)]
        ])

        # Observation matrix: only T can be measured
        C = sp.Matrix([[0.0, 1.0]])

        # Replace constants and get numerical matrices
        def replace_constants(m):
            return np.array(m.subs({
                V_heater: HEATER_VOLTAGE,
                i_heater: HEATER_CURRENT,
                C_air: C_air_num,
                G_box: G_box_num,
                C_heater: C_heater_num,
                G_heater: G_heater_num
            })).astype(np.float64)

        A_num, B_num, C_num = map(replace_constants, [A, B, C])

        ct_system = ss(A_num, B_num, C_num, np.array([[0.0, 0.0]]))
        dt_system = ct_system.sample(step_size, method="backward_diff")

        f = KalmanFilter(dim_x=2, dim_z=1, dim_u=2)
        f.x = np.array([[initial_heat_temperature],  # T_heater at t=0
                        [initial_box_temperature]])  # T at t=0
        f.F = dt_system.A
        f.B = dt_system.B
        f.H = dt_system.C
        f.P = np.array([[100., 0.],
                        [0., 100.]])
        f.R = np.array([[std_dev]])
        f.Q = Q_discrete_white_noise(dim=2, dt=step_size, var=std_dev ** 2)

        return f


