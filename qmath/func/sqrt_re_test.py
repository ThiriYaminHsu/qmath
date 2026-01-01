from qmath.func.sqrt import Sqrt
from qmath.utils.re_utils import re_numeric_fixed_point, re_symbolic_fixed_point, verify_re
import pytest
import os

RUN_SLOW_TESTS = os.getenv("RUN_SLOW_TESTS") == "1"


# @pytest.mark.skipif(not RUN_SLOW_TESTS, reason="slow test")
@pytest.mark.parametrize("half_arg", [False, True])
def test_re_sqrt(half_arg: bool):
    op = Sqrt(half_arg=False)
    re_symbolic = re_symbolic_fixed_point(op)
    re_numeric = lambda assgn: re_numeric_fixed_point(op, assgn)
    for n in [5, 6, 7, 20, 21]:
        for radix in [0, 1, 2]:
            verify_re(re_symbolic, re_numeric, {"n": n, "radix": radix})
