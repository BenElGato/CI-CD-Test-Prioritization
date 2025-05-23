def is_palindrome(s: str) -> bool:
    """Check if a string is a palindrome."""
    s = s.lower().replace(" ", "")
    return s == s[::-1]

def reverse_words(sentence: str) -> str:
    """Reverse the order of words in a sentence."""
    return " ".join(reversed(sentence.split()))

def count_vowels(s: str) -> int:
    """Count the number of vowels in a string."""
    return sum(1 for char in s.lower() if char in "aeiou")