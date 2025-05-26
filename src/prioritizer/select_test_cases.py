import os
import json
from typing import List

from src.objectives.CoverageOnDIffs import compute_diff_coverage
from src.objectives.ExecutionTime import get_test_execution_times, save_test_execution_times
from src.objectives.FailureRates import get_failure_rates, simulate_historic_failure_rates
from src.objectives.TotalCoverage import compute_total_coverage, get_total_coverage
from src.prioritizer.greedy import greedy_select, prioritize_coverage, \
    prioritize_execution_time, prioritize_fault_detection
from src.prioritizer.diff_parser import get_changed_files_and_lines_mock
import config


def get_all_test_files(test_dir: str) -> list:
    test_files = []
    for root, _, files in os.walk(test_dir):
        for file in files:
            if file.startswith("test_") and file.endswith(".py"):
                test_files.append(os.path.join(root, file))
    test_files.sort()
    return test_files

def get_all_source_files(source_dir: str) -> list:
    test_files = []
    for root, _, files in os.walk(source_dir):
        for file in files:
            if not file.startswith("test_") and file.endswith(".py"):
                test_files.append(os.path.join(root, file))
    test_files.sort()
    return test_files

def save_file_mapping(test_files: List[str], output_path: str):
    mapping = {str(i): test_file for i, test_file in enumerate(test_files)}

    with open(output_path, 'w') as f:
        json.dump(mapping, f, indent=4)

    print(f"Saved mapping of {len(test_files)} test files to: {output_path}")

def save_objective_data():
    '''
    Compute and save the objective data for the prioritization algorithm
    :return:
    '''
    test_files = get_all_test_files(config.TEST_FOLDER)
    source_files = get_all_source_files(config.TARGET_FOLDER)
    matrix, test_ids, code_lines = compute_total_coverage(test_files, source_files)
    # TODO
    test_execution_times = save_test_execution_times(test_files)
    simulate_historic_failure_rates(test_ids)


def select_test_cases(budget: int, changes: str) -> tuple[list, list, list, list]:
    # Extract objective information
    matrix, test_ids, code_lines = get_total_coverage()
    diff_matrix, diff_code_lines = compute_diff_coverage(matrix, test_ids, code_lines, changes)
    # TODO
    test_execution_times = get_test_execution_times(test_ids)
    test_failure_rates = get_failure_rates(test_ids)

    # Select the test cases
    tests_full_coverage = greedy_select(test_ids, budget, prioritize_coverage, matrix)
    tests_diff_coverage = greedy_select(test_ids, budget, prioritize_coverage, diff_matrix)
    #reduced_test_set_coverage_per_cost = greedy_select(test_ids, budget, prioritize_execution_time, test_execution_times)
    tests_execution_time = None
    tests_failure_rates = greedy_select(test_ids, budget, prioritize_fault_detection, test_failure_rates)

    return tests_full_coverage, tests_diff_coverage, tests_execution_time, tests_failure_rates

if __name__ == "__main__":
    budget = 7
    save_objective_data()
    changes = get_changed_files_and_lines_mock(f"{config.DIFF_FOLDER}/calculator_1.txt")
    reduced_test_set_full_coverage, reduced_test_set_diff_coverage, reduced_test_set_coverage_per_cost, reduced_test_set_failure_rates = select_test_cases(budget, changes)
    print(f"Full coverage: {reduced_test_set_full_coverage}")
    print(f"Diff coverage: {reduced_test_set_diff_coverage}")
    print(f"Coverage per cost: {reduced_test_set_coverage_per_cost}")
    print(f"Fault detection: {reduced_test_set_failure_rates}")



