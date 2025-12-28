from psiqworkbench import QPU, QFixed, Qubits, Qubrick, QUInt, SymbolicQPU, SymbolicQubits, resource_estimator


class SymbolicQFixed(SymbolicQubits):
    """Symbolic register for fixed-precision signed number."""

    def __init__(self, *, radix: int = 0, **kwargs):
        super().__init__(**kwargs)
        self.radix = radix


def alloc_temp_qreg_like(qbk: Qubrick, x: QFixed, name: str = "") -> tuple[Qubits, QFixed]:
    """Allocates temporary register with the same size and radix as x.

    Returns pair of raw .... (todo: comment after check that maybe not need pair.)
    Also is correct in symbolic computation.
    """
    if name == "":
        name = x.name + "_clone"
    qreg = qbk.alloc_temp_qreg(x.num_qubits, name)
    if x.qpu.is_symbolic:
        return qreg, SymbolicQFixed(num_qubits=x.num_qubits, name=name, radix=x.radix, qpu=x.qpu)
    else:
        return qreg, QFixed(qreg, radix=x.radix, qpu=x.qpu)
