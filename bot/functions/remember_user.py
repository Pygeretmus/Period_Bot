async def remember_user(self, user) -> None:
    """
    Saving user into internal dictionary
    """
    self.all_users[user.user_id] = user
