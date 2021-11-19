import pickle
from fmi2 import Fmi2FMU, Fmi2Status


class Model(Fmi2FMU):
    def __init__(self, reference_to_attr=None) -> None:
        super().__init__(reference_to_attr)
        self.T_heater = 0.0
        self.T_bair = 0.0

        self._update_outputs()

    def serialize(self):

        bytes = pickle.dumps(
            (
                self.T_heater,
                self.T_bair,
            )
        )
        return Fmi2Status.ok, bytes

    def deserialize(self, bytes) -> int:
        (
            T_heater,
            T_bair,
        ) = pickle.loads(bytes)
        self.T_heater = T_heater
        self.T_bair = T_bair
        self._update_outputs()

        return Fmi2Status.ok

    def _update_outputs(self):
        #anomaly detector logic will be added here
        self.enable = True

    def do_step(self, current_time, step_size, no_step_prior):

        self._update_outputs()

        return Fmi2Status.ok

