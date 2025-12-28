from qmath.func.square import Square
from qmath.utils.re_utils import re_numeric_fixed_point, re_symbolic_fixed_point, verify_re


def test_re_square():
    op = Square()
    re_symbolic = re_symbolic_fixed_point(op, n_inputs=2)
    re_numeric = lambda assgn: re_numeric_fixed_point(op, assgn, n_inputs=2)
    for n, radix in [(10, 1), (10, 5), (10, 9)]:
        verify_re(re_symbolic, re_numeric, {"n": n, "radix": radix}, av_rtol=0.001)
