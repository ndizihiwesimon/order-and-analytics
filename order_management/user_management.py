from __future__ import annotations

from .user import User
from typing import List


class UserManagement:
    """Main class to manage the user accounts

    Attributes:
        users: A list of users
        status_file: file where log ins are recorded
    """

    def __init__(
        self, status_file: str = "data/.logged_in", users: List[User] = []
    ) -> None:
        self.users = users
        self.status_file = status_file

    def get_logged_in_user(self) -> User:
        """Returns the logged in user"""

        # Reads the file and returns the user
        try:
            with open(self.status_file, "r") as f:
                username = (
                    f.readline().strip()
                )  # Assuming the first line contains the username
                for user in self.users:
                    if user.username == username:
                        return user
                raise Exception("No logged-in user found")
        except FileNotFoundError:
            raise Exception("Status file not found")

    def get_user_details(self, username: str) -> User:
        """Returns the account of a user

        Args:
            username: the target username
        """
        # Loop through the loaded accounts and return the one with the right username
        for user in self.users:
            if user.username == username:
                return user
        raise Exception("User not found")

    @staticmethod
    def load(inFile: str = "data/credentials.txt") -> UserManagement:
        """Loads the accounts from a file"""

        # open the file and retrieve the relevant fields to create the objects.
        with open(inFile, "r") as f:
            users = [
                User(elements[0], elements[3], elements[4], bool(elements[5]))
                for line in f.readlines()
                if (elements := line.strip().split(":"))
            ]
            return UserManagement(users=users)
