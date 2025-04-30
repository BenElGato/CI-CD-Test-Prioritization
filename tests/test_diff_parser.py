import subprocess
import pytest
from src.prioritizer.diff_parser import parse_diff, get_changed_files_and_lines

# Sample unified diff for testing
SIMPLE_DIFF = '''diff --git a/foo.py b/foo.py
index abcdef1..abcdef2 100644
--- a/foo.py
+++ b/foo.py
@@ -1,3 +1,4 @@
 line1
+added_line
 line2
-line3
'''  # added at line 2, removed old line3, context line2

MULTI_FILE_DIFF = '''diff --git a/foo.py b/foo.py
index 111..222 100644
--- a/foo.py
+++ b/foo.py
@@ -10,2 +10,3 @@
 context1
+new1
 context2
@@ -20 +20,0 @@
-line_to_remove
diff --git a/bar.py b/bar.py
index aaa..bbb 100644
--- a/bar.py
+++ b/bar.py
@@ -5 +5,2 @@
-line_old
+line_new1
+line_new2
'''  # foo.py adds at lines 11, bar.py adds at lines 5 and 6


def test_parse_diff_simple():
    changes = parse_diff(SIMPLE_DIFF)
    # foo.py should have one added line at new file line 2
    assert 'foo.py' in changes
    assert changes['foo.py'] == {2}


def test_parse_diff_multi_file():
    changes = parse_diff(MULTI_FILE_DIFF)
    # foo.py: new hunk at +10,3 => lines 10,11,12 but only new lines with '+'
    # In the first hunk, only one '+' before new1 => line 11
    # Second hunk is a removal, no '+' lines
    assert changes['foo.py'] == {11}

    # bar.py: one hunk with two '+' lines starting at +5 => lines 5 and 6
    assert 'bar.py' in changes
    assert changes['bar.py'] == {5, 6}


def test_parse_diff_no_changes():
    empty = parse_diff('')
    assert empty == {}


def test_get_changed_files_and_lines_monkeypatch(monkeypatch):
    # Monkeypatch subprocess.run to return SIMPLE_DIFF
    class DummyProc:
        def __init__(self):
            self.stdout = SIMPLE_DIFF
            self.stderr = ''
    def fake_run(cmd, stdout, stderr, text, check):
        return DummyProc()

    monkeypatch.setattr(subprocess, 'run', fake_run)
    changes = get_changed_files_and_lines(base='A', head='B')
    assert changes == {'foo.py': {2}}


def test_hunk_header_without_count():
    # Hunk header with no count defaults to 1 line
    diff = '''diff --git a/x.py b/x.py
--- a/x.py
+++ b/x.py
@@ -5 +5 @@
+only_line
'''  # +5 with no count => new_line_num start 5, then + line => 6
    changes = parse_diff(diff)
    assert changes['x.py'] == {6}
