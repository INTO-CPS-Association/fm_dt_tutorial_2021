import pickle
from fmi2 import Fmi2FMU, Fmi2Status


class Model(Fmi2FMU):
    def __init__(self, reference_to_attr=None) -> None:
        super().__init__(reference_to_attr)
        self.T_room_out = 20

    def do_step(self, current_time, step_size, no_step_prior):

        return Fmi2Status.ok

