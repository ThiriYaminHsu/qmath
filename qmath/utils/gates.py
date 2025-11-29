from psiqworkbench import Qubits

from typing import Optional


def cnot(a: Qubits, b: Qubits, ctrl: Optional[Qubits] = None):
    assert len(a) == len(b) == 1
    b.x(a | ctrl)


def ccnot(a: Qubits, b: Qubits, c: Qubits, ctrl: Optional[Qubits] = None):
    assert len(a) == len(b) == len(c) == 1
    c.x(a | b | ctrl)


def controlled_swap(ctrl: Qubits, a: Qubits, b: Qubits):
    assert len(ctrl) == len(a) == len(b) == 1
    b.x(a)
    a.x(b | ctrl)
    b.x(a)
