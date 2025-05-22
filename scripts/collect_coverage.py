import uuid
import coverage
import numpy as np
import importlib.util
import sys
from types import ModuleType
from typing import Callable, Tuple
import inspect
import os
import ast
from typing import List

def load_module_from_file(filepath: str) -> ModuleType:
    """Dynamically load a Python module from a file."""
    module_name = f"dynamic_module_{uuid.uuid4().hex}"
    spec = importlib.util.spec_from_file_location(module_name, filepath)
    module = importlib.util.module_from_spec(spec)
    sys.modules[module_name] = module
    spec.loader.exec_module(module)
    return module

def get_all_coverable_lines(source_file: str) -> List[int]:
    """Parse the source with ast and return every node.lineno you can find."""
    with open(source_file, "r") as f:
        tree = ast.parse(f.read(), filename=source_file)

    all_lines = {
        node.lineno
        for node in ast.walk(tree)
        if hasattr(node, "lineno")
    }
    return sorted(all_lines)

def get_coverage_for_test(test_func: Callable, source_file: str, all_lines: List[int]) -> np.ndarray:
    """Run a single test and get the coverage vector."""
    cov = coverage.Coverage()
    cov.start()
    test_func()
    cov.stop()
    cov.save()

    filename, statements, excluded, missing, _ = cov.analysis2(source_file)
    executed_lines = [lineno for lineno in statements if lineno not in missing]

    return np.array([1 if line in executed_lines else 0 for line in all_lines])


def build_coverage_matrix(test_funcs: List[Callable], source_file: str) -> (np.ndarray, List[int]):
    """Build the full coverage matrix from a list of test functions."""
    all_lines = get_all_coverable_lines(source_file)
    matrix = np.zeros((len(test_funcs), len(all_lines)), dtype=int)

    for i, func in enumerate(test_funcs):
        matrix[i] = get_coverage_for_test(func, source_file, all_lines)
    return matrix, all_lines

def build_coverage_matrix_from_files(
    source_path: str,
    tests_path: str,
) -> Tuple[np.ndarray, List[int], List[str]]:
    """
    Load tests and build a coverage matrix.

    Returns:
        matrix: 2D numpy array (tests x lines)
        lines: sorted list of all coverable line numbers
        test_names: list of test function names in the same order as matrix rows
    """
    # prepare import paths
    test_dir = os.path.dirname(os.path.abspath(tests_path))
    source_dir = os.path.dirname(os.path.abspath(source_path))
    sys.path.insert(0, test_dir)
    sys.path.insert(0, source_dir)

    # load and discover test functions
    test_module = load_module_from_file(tests_path)
    test_funcs = []
    test_names = []
    for name, func in inspect.getmembers(test_module, inspect.isfunction):
        if name.startswith("test_"):
            test_funcs.append(func)
            test_names.append(name)

    if not test_funcs:
        raise RuntimeError("No test functions found in {}".format(tests_path))

    # find all lines and build matrix
    all_lines = get_all_coverable_lines(source_path)
    matrix = np.zeros((len(test_funcs), len(all_lines)), dtype=int)
    for idx, func in enumerate(test_funcs):
        matrix[idx] = get_coverage_for_test(func, source_path, all_lines)

    return matrix, all_lines, test_names