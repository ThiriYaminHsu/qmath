"""Quantum algorithms for evaluating polynomials and polynomial approximations."""

import os
import random

import numpy as np
import pytest
from psiqworkbench import QPU, QFixed
from psiqworkbench.filter_presets import BIT_DEFAULT

from qmath.poly import HornerScheme

RUN_SLOW_TESTS = os.getenv("RUN_SLOW_TESTS") == "1"


@pytest.mark.parametrize("coefs", [[2], [-2, 3.5], [3.5, 2.5, -1]])
def test_horner_linear(coefs: list[float]):
    qpu = QPU(filters=BIT_DEFAULT)
    qpu.reset(100)
    hs = HornerScheme(coefs)
    qx = QFixed(8, name="qx", radix=4, qpu=qpu)
    x = 1.25
    qx.write(x)
    with hs.computed(qx):
        result = hs.get_result_qreg().read()
    assert result == np.polyval(coefs[::-1], x)


@pytest.mark.skipif(not RUN_SLOW_TESTS, reason="slow test")
def test_horner_random():
    qpu = QPU(filters=[">>64bit>>", ">>bit-sim>>"])
    qpu.reset(500)
    coefs = [5.1, -4.2, 0.8]
    num_trials = 2

    for _ in range(num_trials):
        x = -10 + 20 * random.random()
        hs = HornerScheme(coefs)
        qx = QFixed(30, name="qx", radix=16, qpu=qpu)
        qx.write(x)
        hs.compute(qx)
        result = hs.get_result_qreg().read()
        hs.uncompute()
        expected = sum(k * x**i for i, k in enumerate(coefs))
        assert np.isclose(result, expected, atol=1e-3)
