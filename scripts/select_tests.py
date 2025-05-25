import pandas as pd

def select_tests(coverage_csv, changed_files):
    df = pd.read_csv(coverage_csv, index_col=0)
    selected_tests = set()

    for changed_file in changed_files:
        for col in df.columns:
            if col.startswith(changed_file + ":"):
                tests_that_cover = df[df[col] == 1].index.tolist()
                selected_tests.update(tests_that_cover)

    return list(selected_tests)

if __name__ == "__main__":
    coverage_csv = "data/coverage_matrix.csv"
    changed_files = [line.strip() for line in open("changed_files.txt") if line.strip()]
    selected_tests = select_tests(coverage_csv, changed_files)
    with open(".selected_tests", "w") as f:
        f.write("\n".join(selected_tests))


# output sample:
# test_file1.py::test_add
# test_file2.py::test_cube