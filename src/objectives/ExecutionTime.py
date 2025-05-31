import csv
import os
import subprocess
import time
from typing import List

import numpy as np

import config


def save_test_execution_times(test_ids: List[str]) -> None:
    """
    Measure and save execution times for each test in the provided list.

    :param test_ids: List of pytest-style test identifiers (e.g. "test_module::test_func")
    """
    results = []

    for test_id in test_ids:
        start = time.perf_counter()

        try:
            subprocess.run(
                ["pytest", "-q", test_id, "--disable-warnings"],
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
                check=False  # Allow test failure; we only care about timing
            )
        except Exception as e:
            print(f"Failed to run {test_id}: {e}")
            continue

        end = time.perf_counter()
        duration = end - start
        results.append((test_id, duration))

    # Ensure folder exists
    os.makedirs(config.MATRIX_FOLDER, exist_ok=True)
    output_path = os.path.join(config.MATRIX_FOLDER, "execution_times.csv")

    with open(output_path, mode="w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(["test_id", "execution_time"])
        writer.writerows(results)

def get_test_execution_times(test_ids: List[str]) -> np.ndarray:
    """
    Retrieve execution times for the given test IDs from the CSV file.

    :param test_ids: List of test identifiers (e.g., 'test_file.py::test_name')
    :return: List of execution times in the same order as test_ids
    """
    execution_times = {}
    csv_path = os.path.join(config.MATRIX_FOLDER, "execution_times.csv")

    if not os.path.exists(csv_path):
        raise FileNotFoundError(f"Execution times file not found at: {csv_path}")

    # Load all recorded times into a dictionary
    with open(csv_path, mode="r", newline="") as file:
        reader = csv.DictReader(file)
        for row in reader:
            test_id = row["test_id"]
            time_val = float(row["execution_time"])
            execution_times[test_id] = time_val

    # Return list in order, with 0.0 as fallback if not found
    return np.array([execution_times.get(test_id, 0.0) for test_id in test_ids])