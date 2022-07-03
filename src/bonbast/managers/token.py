import datetime

from bonbast.server import get_token_from_main_page


class Token(object):
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

    @staticmethod
    def generate():
        """
        :return: a new [fresh] Token instance
        """
        try:
            from .storage import storage_manager

        except ImportError:
            from storage import storage_manager

        def build_fresh_token():
            storage_manager.delete_token()
            instance = Token(get_token_from_main_page())
            storage_manager.save_token(instance)

            return instance

        try:
            token_instance = storage_manager.get_token()
        except FileNotFoundError:
            token_instance = build_fresh_token()

        if token_instance.is_expired():
            token_instance = build_fresh_token()

        return token_instance
