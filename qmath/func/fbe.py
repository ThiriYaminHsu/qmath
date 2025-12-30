"""Function-value binary expansion algorithms.

Reference:
    Shengbin Wang, Zhimin Wang, Wendong Li, Lixin Fan, Guolong Cui,
    Zhiqiang Wei, Yongjian Gu.
    Quantum circuits design for evaluating transcendental functions based on a
    function-value binary expansion method.
    https://arxiv.org/abs/2001.00807
"""

import psiqworkbench.qubricks as qbk
from psiqworkbench import QFixed, QInt, QUInt, Qubits
from psiqworkbench.qubricks import Qubrick
from psiqworkbench.qubits.base_qubits import BaseQubits
from psiqworkbench.symbolics.qubrick_costs import QubrickCosts


class CosFbe(Qubrick):
    """Computes cos(pi*x), where x∈[0,1)."""

    def _iteration():
        pass

    def _compute(self, x: QFixed):
        pass
