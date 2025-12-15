from psiqworkbench import QPU


class QPURecorder:
    """A helper for QPU testing.

    It allows to record instructions and re-applying them. Reapplying elementary
    instructions is significantly faster then re-running Qubrick.compute().
    """

    def __init__(self, qpu: QPU):
        self.qpu = qpu
        self.prep = self.qpu.get_instructions()

    def record_computation(self):
        """Stores all instructions from helper construction until now as 'computation'."""
        self.computation = self.qpu.get_instructions()[len(self.prep) :]

    def restore_initial_state(self):
        """Rewinds QPU to the state as when the helper was constructed."""
        self.qpu.clear_instructions()
        self.qpu.put_instructions(self.prep)

    def apply_computation(self):
        """Applies previously stored 'computation'."""
        self.qpu.put_instructions(self.computation)
