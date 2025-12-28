from psiqworkbench import QPU, QFixed, Qubits, Qubrick, QUInt, SymbolicQPU, SymbolicQubits, resource_estimator


class SymbolicQFixed(SymbolicQubits):
    """Symbolic register for fixed-precision signed number."""

    def __init__(self, *, radix: int = 0, **kwargs):
        super().__init__(**kwargs)
        self.radix = radix


class Dummy:
    def release(self):
        pass


def alloc_temp_qreg_like(qbk: Qubrick, x: QFixed, name: str = "") -> tuple[Qubits, QFixed]:
    """Allocates temporary register with the same size and radix as x.

    Returns pair of raw .... (todo: comment after check that maybe not need pair.)
    Also is correct in symbolic computation.
    """
    if name == "":
        name = x.name + "_clone"
    if x.qpu.is_symbolic:
        qreg = qbk.alloc_temp_qreg(x.num_qubits, name)
        qreg.radix = x.radix
        return qreg, qreg  # SymbolicQFixed(num_qubits=x.num_qubits, name=name, radix=x.radix, qpu=x.qpu)
    else:
        qreg = qbk.alloc_temp_qreg(x.num_qubits, name)
        return qreg, QFixed(qreg, radix=x.radix, qpu=x.qpu)
