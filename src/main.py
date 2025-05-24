import os
from scripts.collect_coverage import build_global_coverage_matrix
import json
from typing import List
import pandas as pd
import numpy as np

from src.prioritizer.diff_parser import get_changed_files_and_lines, get_changed_files_and_lines_mock

TARGET_FOLDER = "../dummy_targets"
TEST_FOLDER  = "../dummy_targets/tests"

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

def save_matrix_with_labels(matrix: np.ndarray, test_ids: List[str], code_lines: List[str], output_path: str):
    df = pd.DataFrame(matrix, index=test_ids, columns=code_lines)
    df.to_csv(output_path, sep=",")  # or use ',' for CSV



if __name__ == "__main__":
    # Get all test files and store them in an ordered list
    test_files = get_all_test_files(TEST_FOLDER)
    print(test_files)
    source_files = get_all_source_files(TARGET_FOLDER)
    print(source_files)


    matrix, test_ids, code_lines = build_global_coverage_matrix(source_files, test_files)
    # Save the coverage results
    cleaned_test_ids = [f"{os.path.basename(path.split('::')[0])}::{path.split('::')[1]}" for path in test_ids]
    cleaned_code_line_names = [code_line.split('/')[-1] for code_line in code_lines]
    save_matrix_with_labels(matrix, cleaned_test_ids, cleaned_code_line_names, "../data/coverage_matrix.csv")

    print(matrix)
    print(code_lines)

    coverage_of_lines = matrix.any(axis=0)
    print(coverage_of_lines)

    # TODO: Actually get the diffs to verify behavior!
    #changes = get_changed_files_and_lines("v1.0", "v1.1")
    '''
    Changes will be in the following format:
    {
      "file1.py": {10, 11, 12},
      "folder/file2.md": {15, 16}
    }
    '''
    # For now, get the diffs from dummy diff files
    changes = get_changed_files_and_lines_mock("../dummy_targets/MockDiffs/diff1.txt")

    csv_columns = [f"{file}:{lineno}" for file, lines in changes.items() for lineno in sorted(lines)]
    # Convert NumPy matrix to pandas DataFrame
    matrix_df = pd.DataFrame(matrix, index=cleaned_test_ids, columns=cleaned_code_line_names)
    relevant_columns = [col for col in csv_columns if
                        col in matrix_df.columns]  # Ensure relevant columns exist in DataFrame
    relevant_matrix = matrix_df[relevant_columns]

    save_matrix_with_labels(relevant_matrix, cleaned_test_ids, csv_columns, "../data/relevant_coverage_matrix.csv")

    # TODO: Apply Prioritization Algorithms based on this matrix!




