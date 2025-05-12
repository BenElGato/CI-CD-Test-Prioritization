import uuid
import coverage
import numpy as np
import importlib.util
import sys
from types import ModuleType
from typing import List, Callable
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

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Build a test coverage matrix for Python source code.")
    parser.add_argument("--source", required=True, help="Path to the Python source file (e.g., calculator.py)")
    parser.add_argument("--tests", required=True, help="Path to the test file (e.g., test_calculator.py)")
    args = parser.parse_args()

    # Add this near the top of collect_coverage.py (before importing the test module)
    test_dir = os.path.dirname(os.path.abspath(args.tests))
    source_dir = os.path.dirname(os.path.abspath(args.source))

    # Add both the test and source dirs to sys.path
    sys.path.insert(0, test_dir)
    sys.path.insert(0, source_dir)

    test_module = load_module_from_file(args.tests)
    test_funcs = [func for name, func in inspect.getmembers(test_module, inspect.isfunction)
            if name.startswith("test_")]

    matrix, lines = build_coverage_matrix(test_funcs, args.source)

    print("Coverage matrix (rows = test cases, columns = source lines):")
    print(matrix)
