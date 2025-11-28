from typing import Optional

from psiqworkbench import Qubits, QUInt
from psiqworkbench.interfaces import Adder
from psiqworkbench.interoperability import implements
from psiqworkbench.qubricks import Qubrick

from ..utils.gates import ccnot, cnot
from ..utils.padding import padded


class ApplyOuterTTKAdder(Qubrick):
    def _compute(self, rhs: Qubits, lhs: Qubits, ctrl: Optional[Qubits] = None):
        assert len(rhs) <= len(lhs), "Input register lhs must be at least as long as rhs."
        for i in range(1, len(rhs)):
            cnot(rhs[i], lhs[i], ctrl=ctrl)
        for i in range(len(rhs) - 2, 0, -1):
            cnot(rhs[i], rhs[i + 1], ctrl=ctrl)


class ApplyInnerTTKAdderNoCarry(Qubrick):
    def _compute(self, rhs: Qubits, lhs: Qubits, ctrl: Optional[Qubits] = None):
        assert len(rhs) == len(lhs)
        for idx in range(len(rhs) - 1):
            ccnot(rhs[idx], lhs[idx], rhs[idx + 1])
        for idx in range(len(rhs) - 1, 0, -1):
            cnot(rhs[idx], lhs[idx], ctrl=ctrl)
            ccnot(rhs[idx - 1], lhs[idx - 1], rhs[idx])


class ApplyInnerTTKAdderWithCarry(Qubrick):
    def _compute(self, rhs: Qubits, lhs: Qubits, ctrl: Optional[Qubits] = None):
        n = len(rhs)
        assert n + 1 == len(lhs), "lhs must be one qubit longer then rhs."
        assert n > 0, "rhs should not be empty."
        for idx in range(n - 1):
            ccnot(rhs[idx], lhs[idx], rhs[idx + 1])
        ccnot(rhs[n - 1], lhs[n - 1], lhs[n], ctrl=ctrl)
        for idx in range(n - 1, 0, -1):
            cnot(rhs[idx], lhs[idx], ctrl=ctrl)
            ccnot(rhs[idx - 1], lhs[idx - 1], rhs[idx])


@implements(Adder[QUInt, QUInt])
class TTKAdder(Qubrick):
    """Computes lhs += rhs modulo 2^n using ripple-carry addition algorithm.

    Requires len(rhs) <= len(lhs) = n.

    If len(rhs) <= len(lhs)-2, rhs is padded with 0-initialized qubits.

    Implementation of the adder presented in paper:
        "Quantum Addition Circuits and Unbounded Fan-Out",
        Yasuhiro Takahashi, Seiichiro Tani, Noboru Kunihiro, 2009.
        https://arxiv.org/abs/0910.2530
    """

    def _compute(self, lhs: QUInt, rhs: QUInt, ctrl: Optional[Qubits] = None):
        rhs_len = len(rhs)
        lhs_len = len(lhs)

        assert lhs_len >= rhs_len, "Register `lhs` must be longer than register `rhs`."
        assert rhs_len >= 1, "Registers `rhs` and `lhs` must contain at least one qubit."

        if rhs_len == lhs_len:
            if rhs_len > 1:
                with ApplyOuterTTKAdder().computed(rhs, lhs, ctrl=ctrl):
                    ApplyInnerTTKAdderNoCarry().compute(rhs, lhs, ctrl=ctrl)
            cnot(rhs[0], lhs[0], ctrl=ctrl)
        elif rhs_len + 1 == lhs_len:
            if rhs_len > 1:
                cnot(rhs[rhs_len - 1], lhs[lhs_len - 1], ctrl=ctrl)
                with ApplyOuterTTKAdder().computed(rhs, lhs, ctrl=ctrl):
                    ApplyInnerTTKAdderWithCarry().compute(rhs, lhs, ctrl=ctrl)
            else:
                ccnot(rhs[0], lhs[0], lhs[1], ctrl=ctrl)
            cnot(rhs[0], lhs[0], ctrl=ctrl)
        else:
            assert rhs_len + 2 <= lhs_len
            # Pad rhs so that its length is one qubit shorter than lhs.
            with padded(self, (rhs,), (len(lhs) - 1,)) as (rhs,):
                assert len(rhs) == len(lhs) - 1
                self._compute(lhs, rhs)
