from psiqworkbench import Qubits


def cnot(a: Qubits, b: Qubits):
    assert len(a) == len(b) == 1
    b.x(a)


def ccnot(a: Qubits, b: Qubits, c: Qubits):
    assert len(a) == len(b) == len(c) == 1
    c.x(a | b)


def controlled_swap(ctrl: Qubits, a: Qubits, b: Qubits):
    assert len(ctrl) == len(a) == len(b) == 1
    ccnot(ctrl, a, b)
    ccnot(ctrl, b, a)
    ccnot(ctrl, a, b)
