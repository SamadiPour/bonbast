import datetime

try:
    from ..server import get_token_from_main_page
except:  # noqa
    from src.bonbast.server import get_token_from_main_page


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
            from src.bonbast.managers.storage import storage_manager

        def build_fresh_token():
            storage_manager.delete_token()
            instance = Token(get_token_from_main_page())
            storage_manager.save_token(instance.value, instance.generated_at)

            return instance

        try:
            token_data = storage_manager.get_token()
            token_instance = Token(value=token_data.value, generated_at=token_data.generated_at)
        except FileNotFoundError:
            token_instance = build_fresh_token()

        if token_instance.is_expired():
            token_instance = build_fresh_token()

        return token_instance
