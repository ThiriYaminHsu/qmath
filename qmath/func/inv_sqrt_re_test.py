from qmath.func.inv_sqrt import _InitialGuess, _NewtonIteration, InverseSquareRoot
from qmath.utils.re_utils import re_symbolic_fixed_point, re_numeric_fixed_point, verify_re


def test_re_initial_guess():
    op = _InitialGuess()
    re_symbolic = re_symbolic_fixed_point(op, n_inputs=2)
    re_numeric = lambda assgn: re_numeric_fixed_point(op, assgn, n_inputs=2)
    for n, radix in [(20, 7), (20, 12), (30, 10), (30, 19)]:
        verify_re(re_symbolic, re_numeric, {"n": n, "radix": radix}, no_fail=True)
        print("verify OK")
