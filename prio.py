import argparse
import os

from src.prioritizer.select_test_cases import save_objective_data, select_test_cases, get_changed_files_and_lines_mock

def main():
    parser = argparse.ArgumentParser(description="Process test case selection based on diff and budget.")
    parser.add_argument('--diff', type=str, required=True, help='Path to the diff file')
    parser.add_argument('--budget', type=int, required=True, help='Budget for test selection')
    parser.add_argument('--operator', type=str, choices=['compute', 'extract'], required=True, help='Operation to perform')

    args = parser.parse_args()

    diff_path = args.diff
    budget = args.budget
    operator = args.operator

    if not os.path.exists(diff_path):
        raise FileNotFoundError(f"Diff file not found: {diff_path}")

    if operator == 'compute':
        save_objective_data()
        print("Objective data saved.")
    elif operator == 'extract':
        changes = get_changed_files_and_lines_mock(diff_path)
        (
            tests_full_coverage,
            tests_diff_coverage,
            tests_coverage_per_cost,
            tests_failure_rates,
            tests_nsga2
        ) = select_test_cases(budget, changes)

        print(f"Full coverage: {tests_full_coverage}")
        print(f"Diff coverage: {tests_diff_coverage}")
        print(f"Coverage per cost: {tests_coverage_per_cost}")
        print(f"Fault detection: {tests_failure_rates}")
        print(f"NSGA2: {tests_nsga2}")
    else:
        raise ValueError(f"Unknown operator: {operator}")


if __name__ == "__main__":
    main()
