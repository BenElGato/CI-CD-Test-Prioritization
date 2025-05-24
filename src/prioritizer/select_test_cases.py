import os
import json
from typing import List

from src.Objectives.CoverageOnDIffs import compute_diff_coverage
from src.Objectives.ExecutionTime import get_test_execution_times
from src.Objectives.FailureRates import get_failure_rates
from src.Objectives.TotalCoverage import compute_total_coverage
from src.prioritizer.greedy import greedy_select, prioritize_total_coverage, prioritize_diff_coverage, \
    prioritize_coverage_per_cost, prioritize_fault_detection
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


def select_test_cases(budget: int) -> tuple[list, list, list, list]:
    test_files = get_all_test_files(config.TEST_FOLDER)
    source_files = get_all_source_files(config.TARGET_FOLDER)

    matrix, test_ids, code_lines = compute_total_coverage(test_files, source_files)
    diff_matrix = compute_diff_coverage(matrix, test_ids, code_lines)

    # TODO
    test_execution_times = get_test_execution_times(test_files)

    # TODO
    test_failure_rates = get_failure_rates(test_files)

    # TODO: Implement greedy_select!
    reduced_test_set_full_coverage = greedy_select(test_files, budget, prioritize_total_coverage, matrix)

    reduced_test_set_diff_coverage = greedy_select(test_files, budget, prioritize_diff_coverage, diff_matrix)

    reduced_test_set_coverage_per_cost = greedy_select(test_files, budget, prioritize_coverage_per_cost, test_execution_times)

    reduced_test_set_failure_rates = greedy_select(test_files, budget, prioritize_fault_detection, test_failure_rates)


    return reduced_test_set_full_coverage, reduced_test_set_diff_coverage, reduced_test_set_coverage_per_cost, reduced_test_set_failure_rates

if __name__ == "__main__":
    budget = 100
    reduced_test_set_full_coverage, reduced_test_set_diff_coverage, reduced_test_set_coverage_per_cost, reduced_test_set_failure_rates = select_test_cases(budget)
    print(f"Full coverage: {reduced_test_set_full_coverage}")
    print(f"Diff coverage: {reduced_test_set_diff_coverage}")
    print(f"Coverage per cost: {reduced_test_set_coverage_per_cost}")
    print(f"Fault detection: {reduced_test_set_failure_rates}")



