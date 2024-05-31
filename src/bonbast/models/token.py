import datetime


class Token:
    """
    Represents an authentication token with a limited lifespan.

    Attributes:
        value (str): The value of the token.
        life_span (int): The lifespan of the token in seconds.
        generated_at (datetime.datetime): The datetime when the token was generated.
    """

    def __init__(self, value: str, life_span: int = 600, generated_at: datetime.datetime = datetime.datetime.now()):
        """
        Initializes a new instance of the Token class.

        Args:
            value (str): The value of the token.
            life_span (int): The lifespan of the token in seconds. Defaults to 600.
            generated_at (datetime.datetime): The datetime when the token was generated. Defaults to now.
        """
        self.life_span = life_span
        self.generated_at = generated_at
        self.value = value

    def is_expired(self) -> bool:
        """
        Determines if the token has expired based on its lifespan and generation time.

        Returns:
            bool: True if the token is expired, False otherwise.
        """
        return datetime.datetime.now() - self.generated_at > datetime.timedelta(seconds=self.life_span)
