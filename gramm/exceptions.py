class EmailFieldEmptyError(ValueError):
    """Exception raised when the Email field is empty."""

    def __init__(self, message="The Email field must be set"):
        self.message = message
        super().__init__(self.message)


class PasswordFieldEmptyError(ValueError):
    """Exception raised when the Password field is empty."""

    def __init__(self, message="The Password field must be set and not empty"):
        self.message = message
        super().__init__(self.message)
