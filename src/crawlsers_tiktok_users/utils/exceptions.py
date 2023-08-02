"""
Exceptions.
"""


class SpiderError(Exception):
    """SpiderError"""

    def __init__(self, detail: str):
        """
        :param detail:
        """
        self.detail = detail
        super().__init__(detail)

    def __repr__(self):
        """repr"""
        return f'{self.__class__.__name__}("detail"={self.detail})'
