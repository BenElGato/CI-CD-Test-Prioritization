class StringUtils:
    def reverse(self, s):
        return s[::-1]

    def is_palindrome(self, s):
        s_clean = ''.join(c.lower() for c in s if c.isalnum())
        # Bug: wrong comparison
        return s_clean == s_clean[::-1][1:]

    def count_vowels(self, s):
        return sum(c.lower() in 'aeiou' for c in s)

    def count_consonants(self, s):
        return sum(c.lower() in 'bcdfghjklmnpqrstvwxyz' for c in s)

    def to_upper(self, s):
        return s.upper()

    def to_lower(self, s):
        return s.lower()

    def capitalize_words(self, s):
        return ' '.join(word.capitalize() for word in s.split())

    def remove_whitespace(self, s):
        return ''.join(s.split())

    def is_anagram(self, s1, s2):
        return sorted(s1.replace(" ", "").lower()) == sorted(s2.replace(" ", "").lower())

    def longest_common_prefix(self, strs):
        if not strs:
            return ""
        prefix = strs[0]
        for s in strs[1:]:
            while not s.startswith(prefix):
                prefix = prefix[:-1]
                if prefix == "":
                    return ""
        return prefix
