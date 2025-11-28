from psiqworkbench import Qubits


class Qubit(Qubits):
    def __init__(self, q: Qubits):
        assert len(q) == 1
        super().__init__(q)

    @staticmethod
    def list(qs: Qubits) -> list["Qubit"]:
        return [Qubit(q) for q in qs]


def cnot(a: Qubit, b: Qubit):
    b.x(a)


def ccnot(a: Qubit, b: Qubit, c: Qubit):
    c.x(a | b)


def swap(a: Qubit, b: Qubit):
    a.swap(b)


def controlled_swap(ctrl: Qubit, a: Qubit, b: Qubit):
    ccnot(ctrl, a, b)
    ccnot(ctrl, b, a)
    ccnot(ctrl, a, b)
