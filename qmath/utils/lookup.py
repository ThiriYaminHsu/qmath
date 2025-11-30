from psiqworkbench import QFixed, QUInt, Qubits
from psiqworkbench.qubricks import Qubrick


from typing import Optional


class TableLookup(Qubrick):
    """Assigns target ⊕= table[input].

    Reference: https://arxiv.org/pdf/1805.03662 (fig. 7).
    """

    def _write_number(self, ctrl: Qubits, target: QUInt, number: int):
        # Writes target ⊕= number*ctrl.
        assert 0 <= number < 2**target.num_qubits
        for i in range(target.num_qubits):
            if (number >> i) % 2 == 1:
                target[i].x(ctrl)

    def _lookup_ctrl(self, ctrl: Qubits, address: Optional[Qubits], target: QUInt, table: list[int]):
        if len(table) == 0:
            return
        if address is None:
            self._write_number(ctrl, target, table[0])
            return

        m = len(address)
        assert len(table) <= 2**m

        anc = self.alloc_temp_qreg(1, "anc")
        address[m - 1].x()
        anc.lelbow(ctrl | address[m - 1])
        address[m - 1].x()
        address_rec = address[0 : m - 1] if m > 1 else None
        self._lookup_ctrl(anc, address_rec, target, table[0 : 2 ** (m - 1)])
        anc.x(ctrl)
        self._lookup_ctrl(anc, address_rec, target, table[2 ** (m - 1) :])
        anc.relbow(ctrl | address[m - 1])
        anc.release()

    def _compute(self, address: QUInt, target: QUInt, table: list[int]):
        m = len(address)
        assert 2 ** (m - 1) < len(table), "Address is too long."
        assert len(table) <= 2**m, "Table is too long."
        address[m - 1].x()
        self._lookup_ctrl(address[m - 1], address[0 : m - 1], target, table[0 : 2 ** (m - 1)])
        address[m - 1].x()
        self._lookup_ctrl(address[m - 1], address[0 : m - 1], target, table[2 ** (m - 1) :])
