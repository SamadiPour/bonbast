import datetime


class Token:
    def __init__(self, value: str, life_span: int = 600, generated_at: datetime.datetime = datetime.datetime.now()):
        """
        :param value: token value
        :param life_span: token life span in seconds
        :param generated_at: token generation date
        """
        self.life_span = life_span
        self.generated_at = generated_at
        self.value = value

    def is_expired(self) -> bool:
        """
        :return: True if token is expired
        """
        return datetime.datetime.now() - self.generated_at > datetime.timedelta(seconds=self.life_span)
