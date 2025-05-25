class UserProfile:
    def __init__(self, username, email, age):
        self.username = username
        self.email = email
        self.age = age
        self.friends = []

    def add_friend(self, friend_profile):
        if friend_profile == self:
            raise ValueError("Cannot add yourself as friend")
        if friend_profile not in self.friends:
            self.friends.append(friend_profile)

    def remove_friend(self, friend_profile):
        if friend_profile in self.friends:
            self.friends.remove(friend_profile)

    def is_adult(self):
        # Bug: incorrectly considers age > 18 (should be >=)
        return self.age > 18

    def email_domain(self):
        parts = self.email.split('@')
        if len(parts) != 2:
            raise ValueError("Invalid email")
        return parts[1]

    def friend_count(self):
        return len(self.friends)

    def mutual_friends(self, other_profile):
        return [f for f in self.friends if f in other_profile.friends]
