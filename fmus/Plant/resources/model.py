import pickle
from fmi2 import Fmi2FMU, Fmi2Status
from scipy.integrate import solve_ivp, RK45
import time

HEATER_VOLTAGE = 12.0
HEATER_CURRENT = 10.45

class Model(Fmi2FMU):
    def __init__(self, reference_to_attr=None) -> None:
        super().__init__(reference_to_attr)
        self.T_room_in = 21.0
        self.heater_on_in = False
        self.T_bair_out = 25.0
        self.G_box = 0.73572788
        self.C_air = 68.20829072
        self.C_heater = 243.45802367
        self.G_heater = 0.87095429
        self.T_heater_out = 25.0
        self.delay = -1.0
    
    def state_der(self, t, state):

        # Comment out to remove dummy fault injection that simulates lid opening.
        #G_box = self.G_box if t < 800 else (5*self.G_box if t < 1500 else self.G_box)
        G_box = self.G_box
        (T, T_heater) = state
        
        power_in = HEATER_VOLTAGE * HEATER_CURRENT if self.heater_on_in else 0.0

        power_out_box = G_box * (T - self.T_room_in)

        power_transfer_heat = self.G_heater*(T_heater - T)

        total_power_heater = power_in - power_transfer_heat

        total_power_box = power_transfer_heat - power_out_box

        der_T = (1.0/self.C_air)*(total_power_box)
        der_T_heater = (1.0/self.C_heater)*(total_power_heater)
        return (der_T, der_T_heater)

    def do_step(self, current_time, step_size, no_step_prior):
        
        initial_state = [self.T_bair_out, self.T_heater_out]
        stop_time = current_time + step_size
        self.logger.debug("Invoking internal solver.")
        sol = solve_ivp(
            self.state_der,
            (current_time, stop_time),
            initial_state,
            method=RK45,
            max_step=step_size,
            t_eval=[stop_time],
        )
        
        self.logger.debug(f"Solution success: {sol.success}")
        assert sol.success

        self.logger.debug(f"Getting outputs from internal model: {sol.y}")
        (self.T_bair_out, self.T_heater_out) = sol.y[:,-1]
        self.logger.debug(f"New state: T_bair_out={self.T_bair_out}, T_heater_out={self.T_heater_out}")

        if self.delay > 0.0:
            time.sleep(self.delay)

        return Fmi2Status.ok

