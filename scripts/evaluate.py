import json
import time
from pathlib import Path

# n_tests: total number of tests
# fault_detection_indices: list of indices where faults were (1-based) detected
def compute_apfd(n_tests, fault_detection_indices):
    m = len(fault_detection_indices)
    sum_ranks = sum(fault_detection_indices) - m  # since index starts from 1
    apfd = 1 - (sum_ranks / (n_tests * m)) + (1 / (2 * n_tests))
    return apfd

def compute_change_coverage():
    coverage_path = Path("data/coverage_db.json")

    with open(coverage_path) as f:
        coverage_db = json.load(f)

    # generate from git diff automatically
    changed_lines = {
        "src/runner/runner_core.py": [12, 13, 15],
        "src/prioritizer/selector.py": [20, 21]
    }

    total_changed = 0
    covered_changed = 0

    for filename, lines in changed_lines.items():
        total_changed += len(lines)
        covered_lines = coverage_db.get(filename, [])
        covered_changed += sum(1 for line in lines if line in covered_lines)

    if total_changed == 0:
        return 0.0

    return covered_changed / total_changed

def compute_execution_time():
    return float(Path(".runtime").read_text())

def compute_test_suite_size():
    test_count = len(list(Path("tests").glob("test_*.py")))
    return test_count

if __name__ == "__main__":
    apfd = compute_apfd(n_tests=10, fault_detection_indices=[1, 2, 4])
    coverage = compute_change_coverage()
    time_taken = compute_execution_time()
    suite_size = compute_test_suite_size()

    print(f"APFD: {apfd:.2f}")
    print(f"Coverage of Changes: {coverage:.2f}")
    print(f"Execution Time: {time_taken:.2f} seconds")
    print(f"Test Suite Size: {suite_size} test cases")
