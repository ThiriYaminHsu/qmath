from qmath.benchmarks.benchmarks_test import BENCHMARKS_FILE_NAME, _run_benchmarks

if __name__ == "__main__":
    csv_text = _run_benchmarks()
    with open(BENCHMARKS_FILE_NAME, "w") as f:
        f.write(csv_text)
    print("Benchmarks updated.")
