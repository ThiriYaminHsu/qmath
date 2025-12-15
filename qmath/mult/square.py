import numpy as np
import psiqworkbench.qubricks as qbk
from psiqworkbench import QFixed, QUInt, Qubits
from psiqworkbench.qubricks import Qubrick

from ..utils.gates import parallel_cnot


# TODO: make this more efficient.
# We don't need extra register for copy. See how psiqworkbench.qubricks.Square is implemented.
# TODO: don't take qbk argument.
# TODO: add a test.
def square(x: QFixed, target: QFixed, qubrick: Qubrick) -> QFixed:
    """Computes square of given register."""
    x_reg = Qubits(x)
    x_copy_reg: Qubits = qubrick.alloc_temp_qreg(x.num_qubits, "x_copy")
    x_copy = QFixed(x_copy_reg, radix=x.radix)
    parallel_cnot(x_reg, x_copy_reg)
    qbk.GidneyMultiplyAdd().compute(target, x, x_copy)
    parallel_cnot(x_reg, x_copy_reg)
    x_copy_reg.release()
