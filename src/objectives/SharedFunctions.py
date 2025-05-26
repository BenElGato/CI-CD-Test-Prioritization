from typing import List
import numpy as np
import pandas as pd

def save_matrix_with_labels(matrix: np.ndarray, test_ids: List[str], code_lines: List[str], output_path: str):
    df = pd.DataFrame(matrix, index=test_ids, columns=code_lines)
    df.to_csv(output_path, sep=",")  # or use ',' for CSV