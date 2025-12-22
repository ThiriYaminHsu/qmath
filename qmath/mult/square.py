import numpy as np
import psiqworkbench.qubricks as qbk
from psiqworkbench import QFixed, QUInt, Qubits
from psiqworkbench.qubricks import Qubrick

from ..utils.gates import parallel_cnot


class SquareIteration(Qubrick):
    def _compute(self, a: Qubits, b: Qubits):
        b[0].x(a[0])
        i_max = min(a.num_qubits - 1, b.num_qubits - 2)
        for i in range(1, i_max + 1):
            # TODO: replace with Gidney Elbows.
            b[i + 1].x(a[0] | a[i])


# TODO: make this more efficient.
# We don't need extra register for copy. See how psiqworkbench.qubricks.Square is implemented.
class Square(Qubrick):
    """Computes square of given QFixed register."""

    # TODO: handle sign (if negative, do abs)!

    def _compute_new(self, x: QFixed, target: QFixed) -> QFixed:
        anc = self.alloc_temp_qreg(target.num_qubits, "anc")
        for i in range(x.num_qubits):
            # Where in target to write x[i]^2.
            j = 2 * (i - x.radix) + target.radix
            if j >= target.num_qubits:
                break
            with SquareIteration().computed(x[i:], anc[j:]):
                qbk.GidneyAdd().compute(target[j:], anc[j:])

    def _compute(self, x: QFixed, target: QFixed) -> QFixed:
        x_reg = Qubits(x)
        x_copy_reg: Qubits = self.alloc_temp_qreg(x.num_qubits, "x_copy")
        x_copy = QFixed(x_copy_reg, radix=x.radix)
        parallel_cnot(x_reg, x_copy_reg)
        qbk.GidneyMultiplyAdd().compute(target, x, x_copy)
        parallel_cnot(x_reg, x_copy_reg)
        x_copy_reg.release()
