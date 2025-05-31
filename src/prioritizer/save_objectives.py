import json
import os
from typing import List

from src.objectives.TotalCoverage import compute_total_coverage
from src.objectives.ExecutionTime import save_test_execution_times
from src.objectives.FailureRates import simulate_historic_failure_rates
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
    test_files = get_all_test_files(config.TEST_FOLDER)
    source_files = get_all_source_files(config.TARGET_FOLDER)
    matrix, test_ids, code_lines = compute_total_coverage(test_files, source_files)
    save_test_execution_times(test_ids)
    simulate_historic_failure_rates(test_ids)

if __name__ == "__main__":
    save_objective_data()
