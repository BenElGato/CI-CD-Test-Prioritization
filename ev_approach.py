import csv
from pathlib import Path
from typing import List
import numpy as np
import pandas as pd

import config
from src.prioritizer.diff_parser import get_changed_files_and_lines_mock
from src.prioritizer.select_test_cases import select_test_cases, save_objective_data

def compute_coverage(selected_tests: List[str], coverage_matrix_path: Path) -> float:
    '''
    :param selected_tests: List of paths to test cases.
    :return: Fraction of code lines covered (between 0.0 and 1.0).
    '''
    df = pd.read_csv(coverage_matrix_path, index_col=0)

    # Filter to selected tests only (ensure they're present in the matrix)
    valid_tests = [t for t in selected_tests if t in df.index]
    if not valid_tests:
        return 0.0

    # Extract sub-matrix and compute coverage
    selected_matrix = df.loc[valid_tests].to_numpy().astype(int)
    covered_lines = np.any(selected_matrix, axis=0)  # True if any test covers a line
    coverage = np.sum(covered_lines) / covered_lines.shape[0]
    return coverage

def compute_apfd(test_order: list[str], fault_file_path: str) -> float:
    test_order = [test_id.split("src/tests/")[-1] for test_id in test_order]
    with open(fault_file_path, 'r') as f:
        file_content = f.read()

    local_vars = {}
    exec(file_content, {}, local_vars)
    fault_detection = local_vars["fault_detection"]
    n = len(test_order)

    Ti = []
    for fault, detecting_tests in fault_detection.items():
        # Find the first test in test_order that detects this fault
        positions = [test_order.index(test) + 1 for test in detecting_tests if test in test_order]
        if positions:
            Ti.append(min(positions))  # Only count this fault if detected

    m = len(Ti)  # Only detected faults count toward m

    if m == 0:
        return 0.0  # No faults were detected

    apfd = 1 - (sum(Ti) / (n * m)) + (1 / (2 * n))
    return apfd


def extract_execution_time(test_ids: List[str]) -> float:
    """
    Extracts the sum of execution times of all given test cases from a JSON file.

    :param test_ids: List of test IDs (e.g., relative paths or names).
    :return: Total execution time as a float.
    """
    execution_time_path = Path(f"{config.MATRIX_FOLDER}/execution_times.csv")

    execution_time_data = {}
    with open(execution_time_path, "r", newline="") as f:
        reader = csv.DictReader(f)
        for row in reader:
            test_id = row["test_id"]
            time_val = float(row["execution_time"])
            execution_time_data[test_id] = time_val

    return sum(execution_time_data.get(test_id, 0.0) for test_id in test_ids)

if __name__ == "__main__":
    save_objective_data()
    budget = 20
    change = "calculator_13.txt"
    changes = f"{config.DIFF_FOLDER}/calculator_1.txt"
    changes = get_changed_files_and_lines_mock(changes)
    tests_full_coverage, tests_diff_coverage, tests_execution_time, tests_failure_rates, tests_nsga2, tests_nsga3, tests_spea2 = select_test_cases(budget, changes)
    test_objective_dict = {
        "Full Coverage": tests_full_coverage,
        "Diff Coverage": tests_diff_coverage,
        "Coverage per Cost": tests_execution_time,
        "Fault Detection": tests_failure_rates,
        "NSGA-II": tests_nsga2,
        "NSGA-III": tests_nsga3,
        "SPEA-II": tests_spea2}

    for objective, tests in test_objective_dict.items():
        if tests != None:
            print(f"{objective}: {tests}")
            print("-------------------------")
            total_coverage = compute_coverage(tests, Path(f"{config.MATRIX_FOLDER}/total_coverage_matrix.csv"))
            diff_coverage = compute_coverage(tests, Path(f"{config.MATRIX_FOLDER}/diff_coverage_matrix.csv"))
            apfd = compute_apfd(tests, f"{config.APFD_FOLDER}/{change}")
            time_taken = extract_execution_time(tests)

            print(f"Total Coverage: {total_coverage: .2f}")
            print(f"Coverage of Changes: {diff_coverage:.2f}")
            print(f"APFD: {apfd:.2f}")
            print(f"Execution Time: {time_taken:.2f} seconds")
            print("-------------------------")
