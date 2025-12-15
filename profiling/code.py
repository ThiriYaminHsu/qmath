from psiqworkbench import QPU, QFixed, QUInt
from psiqworkbench.filter_presets import BIT_DEFAULT
import numpy as np

from qmath.poly import EvalFunctionPPA

qpu = QPU(filters=BIT_DEFAULT)
func = EvalFunctionPPA(np.sin, interval=(-1, 1), degree=3, error_tol=1e-4)

x = 0.5

qpu.reset(500)
qx = QFixed(30, name="qx", radix=25, qpu=qpu)
qx.write(x)
func.compute(qx)
result = func.get_result_qreg().read()
assert np.abs(result - np.sin(x)) < 1e-4

print("OK")
metrics = qpu.metrics()
print("Qubits:", metrics["qubit_highwater"])
print("Total num ops:", metrics["total_num_ops"])
