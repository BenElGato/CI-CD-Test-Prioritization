from typing import Tuple

import numpy as np
import pandas as pd

import config
from src.objectives.SharedFunctions import save_matrix_with_labels

def compute_diff_coverage(matrix: np.ndarray, test_ids: list[str], code_lines: list[str], changes: str) -> Tuple[np.ndarray, list[str]]:
    '''
    :param matrix: Coverage matrix of all test cases and lines
    :param test_ids: List of test case identifiers, e.g. "test_file1.py::test_add"
    :param code_lines: List of code lines, e.g. "file1.py:10"
    :param changes: Path to the diff file containing the changes between two versions, e.g. "v1.0" and "v1.1"
    :return: Reduced coverage matrix with only the relevant lines for the diffs and the list of relevant lines
    '''

    csv_columns = [f"{file}:{lineno}" for file, lines in changes.items() for lineno in sorted(lines)]
    cleaned_code_line_names = [code_line.split('src/targets/')[-1] for code_line in csv_columns]
    # Convert NumPy matrix to pandas DataFrame
    matrix_df = pd.DataFrame(matrix, index=test_ids, columns=code_lines)
    relevant_columns = [col for col in cleaned_code_line_names if
                        col in matrix_df.columns]
    diff_matrix = matrix_df[relevant_columns].to_numpy()
    save_matrix_with_labels(diff_matrix, test_ids, relevant_columns, f"{config.MATRIX_FOLDER}/diff_coverage_matrix.csv")
    return diff_matrix, relevant_columns