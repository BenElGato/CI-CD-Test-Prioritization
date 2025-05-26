import json
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
# For apfd we need to know what is wrong which will be tedious....Do we really want to do this?
'''
def compute_apfd(fault_detection_indices, selected_tests):
    coverage_matrix_path = Path(f"{config.MATRIX_FOLDER}/total_coverage_matrix.csv")
    df = pd.read_csv(coverage_matrix_path, index_col=0)

    fault_indices = []
    for col in df.columns:
        for rank, test_name in enumerate(selected_tests, start=1):
            if test_name in df.index and df.loc[test_name, col] == 1:
                fault_indices.append(rank)
                break

    n_tests = len(selected_tests)
    m = len(fault_detection_indices)

    sum_ranks = sum(fault_detection_indices) - m 
    apfd = 1 - (sum_ranks / (n_tests * m)) + (1 / (2 * n_tests))
    return apfd
'''

def extract_execution_time(test_ids: List[str]) -> float:
    """
    Extracts the sum of execution times of all given test cases from a JSON file.

    :param test_ids: List of test IDs (e.g., relative paths or names).
    :return: Total execution time as a float.
    """
    execution_time_path = Path(f"{config.MATRIX_FOLDER}/test_execution_times.json")

    with open(execution_time_path, "r") as f:
        execution_time_data = json.load(f)

    return sum(execution_time_data.get(test_id, 0.0) for test_id in test_ids)

if __name__ == "__main__":
    save_objective_data()
    budget = 7
    changes = "src/diffs/calculator_1.txt"
    changes = get_changed_files_and_lines_mock(changes)
    tests_full_coverage, tests_diff_coverage, tests_execution_time, tests_failure_rates = select_test_cases(budget, changes)
    test_objective_dict = {
        "Full Coverage": tests_full_coverage,
        "Diff Coverage": tests_diff_coverage,
        "Coverage per Cost": tests_execution_time,
        "Fault Detection": tests_failure_rates}

    for objective, tests in test_objective_dict.items():
        if tests != None:
            print(f"{objective}: {tests}")
            print("-------------------------")
            total_coverage = compute_coverage(tests, Path(f"{config.MATRIX_FOLDER}/total_coverage_matrix.csv"))
            diff_coverage = compute_coverage(tests, Path(f"{config.MATRIX_FOLDER}/diff_coverage_matrix.csv"))
            #apfd = compute_apfd(fault_detection_indices=[1, 2, 4], selected_tests=tests)
            #time_taken = extract_execution_time(tests)

            print(f"Total Coverage: {total_coverage: .2f}")
            print(f"Coverage of Changes: {diff_coverage:.2f}")
            #print(f"APFD: {apfd:.2f}")
            #print(f"Execution Time: {time_taken:.2f} seconds")
            print("-------------------------")
