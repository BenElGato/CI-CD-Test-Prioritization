import subprocess
import re
from typing import Dict, Set, List, Optional


def get_diff(base: str = 'HEAD~1', head: str = 'HEAD') -> str:
    """
    Obtain the unified diff between two Git references.

    :param base: The base Git ref (e.g., 'HEAD~1').
    :param head: The target Git ref (e.g., 'HEAD').
    :return: A unified diff string.
    """
    cmd = ['git', 'diff', f'{base}', f'{head}']
    result = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, check=True)
    return result.stdout


def parse_diff(diff_text: str) -> Dict[str, Set[int]]:
    """
    Parse a unified diff and return changed line numbers for each file.

    :param diff_text: Unified diff as a string.
    :return: Mapping from file paths to sets of changed line numbers in the new version.
    """
    file_changes: Dict[str, Set[int]] = {}
    current_file: Optional[str] = None
    # Track the current line number in the new file
    new_line_num = 0

    # Regular expressions for diff headers and hunks
    diff_file_re = re.compile(r'^diff --git a/(.+) b/(.+)$')
    hunk_header_re = re.compile(r'^@@ -\d+(?:,\d+)? \+(\d+)(?:,(\d+))? @@')

    for line in diff_text.splitlines():
        # Detect a new file diff
        m = diff_file_re.match(line)
        if m:
            # Start tracking a new file
            _, new_path = m.groups()
            current_file = new_path
            file_changes[current_file] = set()
            continue

        if current_file is None:
            continue

        # Detect hunk headers
        m = hunk_header_re.match(line)
        if m:
            start = int(m.group(1))
            count = m.group(2)
            # If no explicit count in header, start at the reported line
            if count is None:
                new_line_num = start
            else:
                # If a count is specified, position before first new line
                new_line_num = start - 1
            continue

        # Process lines in the hunk
        if line.startswith('+') and not line.startswith('+++'):
            # This is an added or modified line in the new file
            new_line_num += 1
            file_changes[current_file].add(new_line_num)
        elif line.startswith('-') and not line.startswith('---'):
            # Removed line in old file; don't increment new_line_num
            continue
        else:
            # Context line
            new_line_num += 1

    return file_changes


def get_changed_files_and_lines(base: str = 'HEAD~1', head: str = 'HEAD') -> Dict[str, Set[int]]:
    """
    Convenience wrapper to get changed lines between two refs.
    """
    diff_text = get_diff(base, head)
    return parse_diff(diff_text)


if __name__ == '__main__':
    # Example usage: print changed lines per file
    changes = get_changed_files_and_lines()
    for f, lines in changes.items():
        print(f"{f}: {sorted(lines)}")
