import psiqworkbench.qubricks as qbk
from psiqworkbench import QFixed, Qubrick
from psiqworkbench.symbolics.qubrick_costs import QubrickCosts


class CompareConstGT(Qubrick):
    """Computes (x > value) where value is classical constant."""

    def __init__(self, value: float, **kwargs):
        super().__init__(**kwargs)
        self.value = value

    def _compute(self, x: QFixed):
        cmp = qbk.CompareGT()
        cmp.compute(x, self.value)
        self.set_result_qreg(cmp.get_result_qreg())

    def _estimate(self, x: QFixed):
        num_elbows = x.num_qubits - 1
        ancs = self.alloc_temp_qreg(num_elbows, "ancs")
        self.set_result_qreg(ancs[num_elbows - 1])
        cost = QubrickCosts(
            active_volume=52 * num_elbows,
            gidney_lelbows=num_elbows,
        )
        self.get_qc().add_cost_event(cost)
