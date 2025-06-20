import os
import subprocess
import json
import glob
from collections import defaultdict
import config
import numpy as np

def get_failure_rates(test_ids) -> np.ndarray:
    '''
    :param test_ids: Ids of the test cases in the format of the coverage matrox lines, e.g test_file1.py::test_add
    :return: Numpy-ndarray that represent of failure rates for each test case in the same order as the input test_ids
    '''
    test_ids = [test_id.split("src/tests/")[-1] for test_id in test_ids]
    failure_rates_path = os.path.join(config.FAILURE_RATE_FOLDER, ".failure_rates.json")

    with open(failure_rates_path, "r") as f:
        data = json.load(f)

    failure_rates = []
    for test_id in test_ids:
        num_failed, num_executed = data.get(test_id, (0, 0))
        if num_executed == 0:
            failure_rate = 0.0
        else:
            failure_rate = num_failed / num_executed
        failure_rates.append(failure_rate)
    return np.array(failure_rates)



def simulate_historic_failure_rates(test_ids):
    '''
    Saves the failure rates for the given test cases based on the historic failure rates. (num_failed, num_executed)
    :param test_ids:
    :return:
    '''
    test_ids = [test_id.split("src/tests/")[-1] for test_id in test_ids]
    failure_rate_path = os.path.join(config.FAILURE_RATE_FOLDER, ".failure_rates.json")
    counter = {test_id: [0, 0] for test_id in test_ids}  # {test_id: [num_failed, num_executed]}

    # Apply each diff
    diff_files = sorted(glob.glob(os.path.join(config.DIFF_FOLDER, "*.txt")))
    for diff_file in diff_files:
        reset_codebase()

        # Apply the diff
        with open(diff_file, "r") as df:
            patch_result = subprocess.run(["git", "apply"], stdin=df,
                                          stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        if patch_result.returncode != 0:
            print(f"Failed to apply {diff_file}:\n{patch_result.stderr.decode()}")
            continue

        # Run pytest and capture report
        test_result = subprocess.run(
            ["pytest", "--json-report"], cwd=config.TEST_FOLDER, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

        report_path = os.path.join(config.TEST_FOLDER, ".report.json")
        if not os.path.exists(report_path):
            print("No test report found — skipping.")
            continue

        with open(report_path, "r") as f:
            report = json.load(f)

        for test in report.get("tests", []):
            test_id = test.get("nodeid")
            if test_id in test_ids:
                counter[test_id][1] += 1  # num_executed
                if test.get("outcome") == "failed":
                    counter[test_id][0] += 1  # num_failed
    # Cleanup
    reset_codebase()
    # Save updated failure rates
    with open(failure_rate_path, "w") as f:
        json.dump({k: tuple(v) for k, v in counter.items()}, f, indent=2)
    
    
# Ensure we're starting from a clean Git state each time
def reset_codebase():
    subprocess.run(["git", "restore", ".", "-q"], cwd=config.TARGET_FOLDER, check=True)
    subprocess.run(["git", "clean", "-fd", "-q"], cwd=config.TARGET_FOLDER, check=True)