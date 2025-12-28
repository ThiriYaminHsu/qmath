import os
import random

import pytest

from qmath.func.square import SquareOptimized
from qmath.utils.test_utils import QPUTestHelper

RUN_SLOW_TESTS = os.getenv("RUN_SLOW_TESTS") == "1"


@pytest.mark.skipif(not RUN_SLOW_TESTS, reason="slow test")
def test_square_random_high_precision():
    qpu_helper = QPUTestHelper(num_qubits=500, qubits_per_reg=51, radix=41, num_inputs=2)
    q_x, q_ans = qpu_helper.inputs
    SquareOptimized().compute(q_x, q_ans)
    qpu_helper.record_op(q_ans)

    for _ in range(50):
        x = -10 + 20 * random.random()
        result = qpu_helper.apply_op([x, 0], check_no_side_effect=True)
        assert abs(result - x**2) < 1e-11
