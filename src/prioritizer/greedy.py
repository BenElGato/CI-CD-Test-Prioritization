from typing import List, Callable
import numpy as np

def greedy_select(test_cases: List[str], budget: int, score_fn: Callable, data: np.ndarray) -> List[str]:
    '''
    Greedily selects test cases based on a scoring function.

    :param test_cases: A list of test case identifiers
    :param budget: Maximum number of test cases to select
    :param score_fn: Scoring function returning a list of scores aligned with test_cases
    :param data: A numpy array containing data aligned with test_cases (row i corresponds to test_cases[i])
    :return: List of selected test case identifiers based on greedy score maximization
    '''
    selected = []
    remaining_indices = set(range(len(test_cases)))

    while len(selected) < budget and remaining_indices:
        current_test_cases = [test_cases[i] for i in remaining_indices]
        current_data = np.array([data[i] for i in remaining_indices])
        scores = score_fn(current_test_cases, current_data)

        best_idx_in_current = max(range(len(scores)), key=lambda i: scores[i])
        best_global_idx = list(remaining_indices)[best_idx_in_current]

        selected.append(test_cases[best_global_idx])
        remaining_indices.remove(best_global_idx)

    return selected


def prioritize_coverage(test_cases: List[str], coverage_array: np.ndarray) -> List[int]:
    '''
    Scores test cases by total coverage (sum of elements per row).

    :param test_cases: A list of test case identifiers
    :param coverage_array: 2D numpy array (n_tests x n_code_elements), 1 if covered, 0 otherwise
    :return: List of total coverage scores for each test case
    '''
    return [int(np.sum(coverage_array[i])) for i in range(len(test_cases))]


def prioritize_fault_detection(test_cases: List[str], failure_rates_array: np.ndarray) -> List[float]:
    '''
    Scores test cases based on their failure rate.

    :param test_cases: A list of test case identifiers
    :param failure_rates_array: 1D numpy array with failure rates
    :return: List of failure rate scores
    '''
    return [float(failure_rates_array[i]) for i in range(len(test_cases))]


def prioritize_execution_time(test_cases: List[str], execution_times_array: np.ndarray) -> List[float]:
    '''
    Scores test cases inversely proportional to execution time (faster = higher score).

    :param test_cases: A list of test case identifiers
    :param execution_times_array: 2D numpy array (n_tests x 1) with execution times in seconds
    :return: List of inverted execution times (higher = faster)
    '''
    scores = []
    for i in range(len(test_cases)):
        time = execution_times_array[i]
        score = 1.0 / time if time > 0 else 0.0
        scores.append(score)
    return scores