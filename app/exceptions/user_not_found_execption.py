# app/exceptions.py
class UserNotFoundException(Exception):
    def __init__(self, user_id: str):
        super().__init__(f"No user found for user_id: {user_id}")
