import pytest
from src.targets.string_utils import StringUtils

su = StringUtils()

def test_reverse():
    assert su.reverse("hello") == "olleh"

def test_is_palindrome():
    assert su.is_palindrome("A man a plan a canal Panama")
    assert not su.is_palindrome("hello")

def test_count_vowels_and_consonants():
    s = "Hello World"
    assert su.count_vowels(s) == 3
    assert su.count_consonants(s) == 7

def test_case_conversion():
    s = "Hello"
    assert su.to_upper(s) == "HELLO"
    assert su.to_lower(s) == "hello"
    assert su.capitalize_words("hello world") == "Hello World"

def test_remove_whitespace():
    s = " h e l l o "
    assert su.remove_whitespace(s) == "hello"

def test_is_anagram():
    assert su.is_anagram("listen", "silent")
    assert not su.is_anagram("hello", "world")

def test_longest_common_prefix():
    assert su.longest_common_prefix(["flower", "flow", "flight"]) == "fl"
    assert su.longest_common_prefix(["dog", "racecar", "car"]) == ""
    assert su.longest_common_prefix([]) == ""
