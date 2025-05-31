import csv
from pathlib import Path
from typing import List
import numpy as np
import pandas as pd
import os
from collections import defaultdict

import config
from src.prioritizer.select_test_cases import select_test_cases
from src.prioritizer.save_objectives import save_objective_data

def compute_coverage(selected_tests: List[str], coverage_matrix_path: Path) -> float:
    df = pd.read_csv(coverage_matrix_path, index_col=0)
    valid_tests = [t for t in selected_tests if t in df.index]
    if not valid_tests:
        return 0.0
    selected_matrix = df.loc[valid_tests].to_numpy().astype(int)
    covered_lines = np.any(selected_matrix, axis=0)
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
    Ti = [min([test_order.index(test) + 1 for test in detecting_tests if test in test_order])
          for fault, detecting_tests in fault_detection.items() if any(test in test_order for test in detecting_tests)]
    m = len(Ti)
    return 0.0 if m == 0 else 1 - (sum(Ti) / (n * m)) + (1 / (2 * n))

def extract_execution_time(test_ids: List[str]) -> float:
    execution_time_path = Path(f"{config.MATRIX_FOLDER}/execution_times.csv")
    execution_time_data = {}
    with open(execution_time_path, "r", newline="") as f:
        reader = csv.DictReader(f)
        for row in reader:
            execution_time_data[row["test_id"]] = float(row["execution_time"])
    return sum(execution_time_data.get(test_id, 0.0) for test_id in test_ids)

if __name__ == "__main__":
    save_objective_data()
    budget = 10
    algorithms = [
        'single_objective_cov', 'single_objective_diff_cov',
        'single_objective_ex_time', 'single_objective_failure_rates',
        'nsga2', 'nsga3', 'spea2'
    ]

    results = defaultdict(lambda: {
        "total_coverage": [], "diff_coverage": [],
        "apfd": [], "execution_time": []
    })

    # Loop over all diff files
    for change_file in os.listdir(config.DIFF_FOLDER):
        if not change_file.endswith(".txt"):
            continue
        changes = f"{config.DIFF_FOLDER}/{change_file}"

        for algorithm in algorithms:
            tests = select_test_cases(budget, changes, algorithm=algorithm)
            total_coverage = compute_coverage(tests, Path(f"{config.MATRIX_FOLDER}/total_coverage_matrix.csv"))
            diff_coverage = compute_coverage(tests, Path(f"{config.MATRIX_FOLDER}/diff_coverage_matrix.csv"))
            apfd = compute_apfd(tests, f"{config.APFD_FOLDER}/{change_file}")
            time_taken = extract_execution_time(tests)

            # Store results
            results[algorithm]["total_coverage"].append(total_coverage)
            results[algorithm]["diff_coverage"].append(diff_coverage)
            results[algorithm]["apfd"].append(apfd)
            results[algorithm]["execution_time"].append(time_taken)

    # Print aggregated results
    print("\n=== Aggregated Results ===")
    for algorithm, metrics in results.items():
        print(f"\nAlgorithm: {algorithm}")
        print(f"Avg Total Coverage:     {np.mean(metrics['total_coverage']):.2f}")
        print(f"Avg Diff Coverage:      {np.mean(metrics['diff_coverage']):.2f}")
        print(f"Avg APFD:               {np.mean(metrics['apfd']):.2f}")
        print(f"Avg Execution Time (s): {np.mean(metrics['execution_time']):.2f}")
