import pickle
from fmi2 import Fmi2FMU, Fmi2Status


class Model(Fmi2FMU):
    def __init__(self, reference_to_attr=None) -> None:
        super().__init__(reference_to_attr)
        self.LL_in = -1.0
        self.UL_in = -1.0
        self.H_in = -1.0
        self.C_in = -1.0
        self.T_bair_in = -1.0
        self.heater_on_out = False
        self.T_desired = 35.0
        self.next_time = 0.0
        self.current_state = "CoolingDown"
    
    def exit_initialization_mode(self):
        
        # Ensure correct initialization
        assert self.LL_in >= 0.0
        assert self.UL_in >= 0.0
        assert self.H_in >= 0.0
        assert self.C_in >= 0.0
        #assert self.T_bair_in >= 0.0

        return Fmi2Status.ok

    def ctrl_step(self, time):
        if self.current_state == "CoolingDown":
            self.heater_on_out = False
            if self.H_in > 0.0 and self.T_bair_in <= self.T_desired - self.LL_in:
                self.current_state = "Heating"
                self.next_time = time + self.H_in
            return
        if self.current_state == "Heating":
            self.heater_on_out = True
            if self.C_in > 0.0 and  0 < self.next_time <= time:
                self.current_state = "Waiting"
                self.next_time = time + self.C_in
            return
        if self.current_state == "Waiting":
            self.heater_on_out = False
            if 0 < self.next_time <= time:
                if self.H_in > 0.0 and self.T_bair_in <= self.T_desired:
                    self.current_state = "Heating"
                    self.next_time = time + self.H_in
                else:
                    self.current_state = "CoolingDown"
                    self.next_time = -1
            return

    def do_step(self, current_time, step_size, no_step_prior):
        self.ctrl_step(current_time)

        self.logger.debug(f"T_bair_in({current_time}) = {self.T_bair_in}")

        return Fmi2Status.ok

