from contextlib import contextmanager
from psiqworkbench import Qubits, Qubrick


@contextmanager
def padded(qbk: Qubrick, registers: tuple[Qubits], padded_lengths: tuple[int]):
    """Pads `registers` with zero qubits (from most significant side) to lengths in `padded_lengths`."""
    assert len(registers) == len(padded_lengths)
    temp_qubits = []
    padded_registers = []
    for i in range(len(registers)):
        assert len(registers[i]) <= padded_lengths[i]
        if len(registers[i]) == padded_lengths[i]:
            padded_registers.append(registers[i])
        else:
            padding: Qubits = qbk.alloc_temp_qreg(padded_lengths[i] - len(registers[i]), f"padding_{i}")
            padded_registers.append(registers[i] | padding)
            temp_qubits.append(padding)
    yield tuple(padded_registers)
    for temp in temp_qubits:
        temp.release()
