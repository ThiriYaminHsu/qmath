from psiqworkbench import Qubits

from typing import Optional


def cnot(a: Qubits, b: Qubits, ctrl: Optional[Qubits] = None):
    assert len(a) == len(b) == 1
    if ctrl is not None:
        b.x(a | ctrl)
    else:
        b.x(a)


def ccnot(a: Qubits, b: Qubits, c: Qubits, ctrl: Optional[Qubits] = None):
    assert len(a) == len(b) == len(c) == 1
    if ctrl is not None:
        c.x(a | b | ctrl)
    else:
        c.x(a | b)


def controlled_swap(ctrl: Qubits, a: Qubits, b: Qubits):
    assert len(ctrl) == len(a) == len(b) == 1
    ccnot(ctrl, a, b)
    ccnot(ctrl, b, a)
    ccnot(ctrl, a, b)
