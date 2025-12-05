from psiqworkbench import QPU, QUInt
from psiqworkbench.filter_presets import BIT_DEFAULT

from qmath.utils.lookup import TableLookup


def test_table_lookup():
    tables = [[1, 8, 7, 9, 15, 0, 3, 4], [8, 4, 9, 0, 0, 1, 1]]
    qpu = QPU(filters=BIT_DEFAULT)
    qpu.reset(9)
    address = QUInt(3, name="address", qpu=qpu)
    target = QUInt(4, name="target", qpu=qpu)
    for table in tables:
        for i in range(len(table)):
            address.write(i)
            target.write(0)
            TableLookup().compute(address, target, table)
            assert target.read() == table[i]
