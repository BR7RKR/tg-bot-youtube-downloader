class MissingTgClientError(Exception):
    def __init__(self, class_name: str):
        message: str = f"Missing tg client in {class_name}"
        super().__init__(message)


class NegativeTimeError(Exception):
    def __init__(self):
        message: str = f"Time value is negative"
        super().__init__(message)
