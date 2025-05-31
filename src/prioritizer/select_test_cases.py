from typing import List
from src.objectives.CoverageOnDIffs import compute_diff_coverage
from src.objectives.ExecutionTime import get_test_execution_times
from src.objectives.FailureRates import get_failure_rates
from src.objectives.TotalCoverage import get_total_coverage
from src.prioritizer.greedy import greedy_select, prioritize_coverage, \
    prioritize_execution_time, prioritize_fault_detection
from src.prioritizer.multi_objective import multiobjective_select


def select_test_cases(budget: int, changes: str, algorithm: str) -> List[str]:
    # Extract objective information
    matrix, test_ids, code_lines = get_total_coverage()
    diff_matrix, diff_code_lines = compute_diff_coverage(matrix, test_ids, code_lines, changes)
    execution_times = get_test_execution_times(test_ids)
    test_failure_rates = get_failure_rates(test_ids)

    if algorithm == "single_objective_cov":
        return greedy_select(test_ids, budget, prioritize_coverage, matrix)
    elif algorithm == "single_objective_diff_cov":
        return greedy_select(test_ids, budget, prioritize_coverage, diff_matrix)
    elif algorithm == "single_objective_ex_time":
        return greedy_select(test_ids, budget, prioritize_execution_time, execution_times)
    elif algorithm == "single_objective_failure_rates":
        return greedy_select(test_ids, budget, prioritize_fault_detection, test_failure_rates)
    elif algorithm in ["nsga2", "nsga3", "spea2", "moead"]:
        return multiobjective_select(
            test_cases=test_ids,
            budget=budget,
            coverage=matrix,
            diff_coverage=diff_matrix,
            execution_time=execution_times,
            failure_rates=test_failure_rates,
            algorithm_name=algorithm
        )
    else:
        # default
        return greedy_select(test_ids, budget, prioritize_coverage, matrix)

def main():
    import argparse

    parser = argparse.ArgumentParser(description="Select test cases based on budget and algorithm.")
    parser.add_argument("--budget", type=int, required=True, help="The time budget for test execution")
    parser.add_argument("--changes", type=str, required=True, help="Code changes as a string")
    parser.add_argument("--algorithm", type=str, required=True, help="Selection algorithm to use")

    args = parser.parse_args()

    selected_tests = select_test_cases(args.budget, args.changes, args.algorithm)
    print("Selected Test Cases:", selected_tests)
    with open("selected_tests.txt", "w") as f:
        for test_file in selected_tests:
            f.write(test_file + "\n")

if __name__ == "__main__":
    main()


