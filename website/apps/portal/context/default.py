from core.util import Callable

class DefaultContext(Callable):
    @staticmethod
    def index(portal: object) -> dict:
        return {
            "default": "O_O",
        }
