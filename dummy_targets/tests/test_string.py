from dummy_targets.string import is_palindrome, reverse_words, count_vowels

def test_is_palindrome():
    assert is_palindrome("Racecar") is True
    assert is_palindrome("Was it a car or a cat I saw") is True
    assert is_palindrome("Hello") is False

def test_reverse_words():
    assert reverse_words("hello world") == "world hello"
    assert reverse_words("one two three") == "three two one"

def test_count_vowels():
    assert count_vowels("hello") == 2
    assert count_vowels("xyz") == 0
    assert count_vowels("AEIOUaeiou") == 10