import random

from psiqworkbench import QPU, QFixed
from psiqworkbench.filter_presets import BIT_DEFAULT

from qmath.add import Subtract
from qmath.utils.test_utils import QPURecorder


def test_subtract():
    qpu = QPU(filters=BIT_DEFAULT)
    qpu.reset(200)
    qs_x = QFixed(40, name="x", radix=30, qpu=qpu)
    qs_y = QFixed(40, name="y", radix=30, qpu=qpu)
    rec = QPURecorder(qpu)
    Subtract().compute(qs_x, qs_y)
    rec.record_computation()

    for _ in range(10):
        x = -100 + 200 * random.random()
        y = -100 + 200 * random.random()

        rec.restore_initial_state()
        qs_x.write(x)
        qs_y.write(y)
        rec.apply_computation()
        result = qs_x.read()
        expected = x - y
        print(x, y, result, expected)
        assert abs(result - expected) < 1e-9
