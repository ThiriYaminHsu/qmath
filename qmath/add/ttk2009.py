from typing import Optional

from psiqworkbench import Qubits, QUInt
from psiqworkbench.interfaces import Adder
from psiqworkbench.interoperability import implements
from psiqworkbench.qubricks import Qubrick


@implements(Adder[QUInt, QUInt])
class TtkAdder(Qubrick):
    """Computes lhs += rhs modulo 2^n using ripple-carry addition algorithm.

    Requires len(rhs) <= len(lhs) = n.

    If Length(rhs) <= Length(lhs)-2, rhs is padded with 0-initialized qubits.

    Implementation of the adder presented in paper:
        "Quantum Addition Circuits and Unbounded Fan-Out",
        Yasuhiro Takahashi, Seiichiro Tani, Noboru Kunihiro, 2009.
        https://arxiv.org/abs/0910.2530
    """

    def _compute(self, lhs: QUInt, rhs: QUInt, ctrl: Optional[Qubits] = None):
        pass
