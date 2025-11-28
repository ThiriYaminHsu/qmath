from psiqworkbench import Qubits, Qubrick


class RotateRight(Qubrick):
    """Rotates qubits in register right by 1."""

    def _compute(self, qs: Qubits):
        k = len(qs)
        k1 = k // 2
        for i in range(k1):
            qs[i].swap(qs[k - 1 - i])
        for i in range(k1 - 1 + (k % 2)):
            qs[i].swap(qs[k - 2 - i])


def rotate_right(qs: Qubits):
    """Rotates qubits in register right by 1."""
    RotateRight().compute(qs)


def rotate_left(qs: Qubits):
    """Rotates qubits in register left by 1."""
    RotateRight().compute(qs, dagger=True)
