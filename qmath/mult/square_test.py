import random

from qmath.mult import Square
from qmath.utils.test_utils import QPUTestHelper


def test_square():
    qpu_helper = QPUTestHelper(num_qubits=200, qubits_per_reg=25, radix=17, num_inputs=2)
    q_x, q_ans = qpu_helper.inputs
    Square().compute(q_x, q_ans)
    qpu_helper.record_op(q_ans)

    for _ in range(50):
        x = -10 + 10 * random.random()
        result = qpu_helper.apply_op([x, 0])
        assert abs(result - x**2) < 1e-4
