import uuid
import coverage
import numpy as np
import importlib.util
import sys
from types import ModuleType
import inspect
import ast
from typing import List, Tuple, Callable
import os

import pandas as pd

import config
from src.Objectives.SharedFunctions import save_matrix_with_labels


def load_module_from_file(filepath: str) -> ModuleType:
    """Dynamically load a Python module from a file."""
    module_name = f"dynamic_module_{uuid.uuid4().hex}"
    spec = importlib.util.spec_from_file_location(module_name, filepath)
    module = importlib.util.module_from_spec(spec)
    sys.modules[module_name] = module
    spec.loader.exec_module(module)
    return module

def get_all_coverable_lines_excluding_defs(source_file: str) -> List[int]:
    with open(source_file, "r") as f:
        tree = ast.parse(f.read(), filename=source_file)

    coverable_lines = set()
    def_lines = set()

    for node in ast.walk(tree):
        if hasattr(node, "lineno"):
            coverable_lines.add(node.lineno)
            if isinstance(node, ast.FunctionDef):
                def_lines.add(node.lineno)

    return sorted(coverable_lines - def_lines)




def get_all_code_lines(source_files: List[str]) -> List[Tuple[str, int]]:
    """Return a list of (file, lineno) for all executable lines."""
    all_lines = []
    for source_file in source_files:
        lines = get_all_coverable_lines_excluding_defs(source_file)
        all_lines.extend([(os.path.abspath(source_file), line) for line in lines])
    return all_lines

def collect_test_functions(test_files: List[str]) -> List[Tuple[Callable, str]]:
    """Collect all test functions across all test files."""
    test_funcs = []
    for test_file in test_files:
        module = load_module_from_file(test_file)
        for name, func in inspect.getmembers(module, inspect.isfunction):
            if name.startswith("test_"):
                test_id = f"{test_file}::{name}"
                test_funcs.append((func, test_id))
    return test_funcs

def get_flat_coverage_vector(test_func: Callable, all_code_lines: List[Tuple[str, int]]) -> np.ndarray:
    """Get coverage vector for a test function against all files+lines."""
    cov = coverage.Coverage()
    cov.start()
    try:
        test_func()
    except:
        pass # Test cases are allowed to fail!
    cov.stop()
    cov.save()

    covered = set()
    for file in cov.get_data().measured_files():
        filename, statements, excluded, missing, _ = cov.analysis2(file)
        executed = [line for line in get_all_coverable_lines_excluding_defs(file) if line not in missing]
        covered.update((file, line) for line in executed)

    return np.array([1 if line in covered else 0 for line in all_code_lines], dtype=int)


def build_global_coverage_matrix(
    source_files: List[str],
    test_files: List[str]
) -> Tuple[np.ndarray, List[str], List[str]]:
    """
    Build a global coverage matrix for all test functions vs all code lines.

    Returns:
        matrix: 2D array of shape (num_tests, num_code_lines)
        code_lines: list of "filename:lineno" strings
        test_ids: list of "test_file.py::test_func" identifiers
    """
    all_code_lines = get_all_code_lines(source_files)
    test_funcs = collect_test_functions(test_files)

    matrix = np.zeros((len(test_funcs), len(all_code_lines)), dtype=int)
    test_ids = []

    for i, (func, test_id) in enumerate(test_funcs):
        matrix[i] = get_flat_coverage_vector(func, all_code_lines)
        test_ids.append(test_id)

    code_lines = [f"{filename}:{lineno}" for filename, lineno in all_code_lines]

    return matrix, test_ids, code_lines

def compute_total_coverage(test_files: List[str], source_files: List[str]):
    matrix, test_ids, code_lines = build_global_coverage_matrix(source_files, test_files)
    # Save the coverage results
    cleaned_test_ids = [test_id.split("../")[-1] for test_id in test_ids]
    cleaned_code_line_names = [code_line.split('src/targets/')[-1] for code_line in code_lines]
    save_matrix_with_labels(matrix, cleaned_test_ids, cleaned_code_line_names, f"{config.MATRIX_FOLDER}/total_coverage_matrix.csv")
    return matrix, cleaned_test_ids, cleaned_code_line_names
def get_total_coverage() -> Tuple[np.ndarray, List[str], List[str]]:
    '''
    Extract the precomputed coverage matrix from the CSV file
    :return: Coverage matrix, test ids, and code lines
    '''
    matrix_df = pd.read_csv(f"{config.MATRIX_FOLDER}/total_coverage_matrix.csv", delimiter=',', index_col=0)
    matrix = matrix_df.to_numpy()
    return matrix, matrix_df.index, matrix_df.columns