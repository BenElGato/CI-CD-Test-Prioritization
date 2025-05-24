import numpy as np
import pandas as pd

import config
from src.prioritizer.diff_parser import get_changed_files_and_lines_mock
from src.Objectives.SharedFunctions import save_matrix_with_labels

def compute_diff_coverage(matrix: np.ndarray, test_ids: list[str], code_lines: list[str]) -> np.ndarray:
    '''
    :param matrix: Coverage matrix of all test cases and lines
    :param test_ids: List of test case identifiers, e.g. "test_file1.py::test_add"
    :param code_lines: List of code lines, e.g. "file1.py:10"
    :return: Reduced coverage matrix with only the relevant lines for the diffs
    '''
    # TODO: Actually get the diffs to verify behavior!
    # changes = get_changed_files_and_lines("v1.0", "v1.1")
    '''
    Changes will be in the following format:
    {
      "file1.py": {10, 11, 12},
      "folder/file2.md": {15, 16}
    }
    '''
    # For now, get the diffs from dummy diff files
    changes = get_changed_files_and_lines_mock(f"{config.DIFF_FOLDER}/diff1.txt")

    csv_columns = [f"{file}:{lineno}" for file, lines in changes.items() for lineno in sorted(lines)]
    # Convert NumPy matrix to pandas DataFrame
    matrix_df = pd.DataFrame(matrix, index=test_ids, columns=code_lines)
    relevant_columns = [col for col in csv_columns if
                        col in matrix_df.columns]
    diff_matrix = matrix_df[relevant_columns]

    save_matrix_with_labels(diff_matrix, test_ids, csv_columns, f"{config.MATRIX_FOLDER}/diff_coverage_matrix.csv")
    return diff_matrix