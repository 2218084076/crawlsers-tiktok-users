import logging
import os
import time
from pathlib import Path

from crawlsers_tiktok_users.config import settings


class Storage:
    """storage"""
    download_path = Path(settings.DOWNLOAD_PATH)

    def __init__(self):
        self.logger = logging.getLogger(f'{__name__}.{self.__class__.__name__}')

    def save_info(self, id: str, link: str):
        """
        Save the user id and link information
        :param id:
        :param link:
        :return:
        """
        filename = self.download_path / 'tiktok-users.txt'
        timestamp = time.strftime("%Y%m%d%H%M%S", time.localtime())
        content = f'{timestamp} {id} {link}\n'
        try:
            with open(filename.resolve(), 'a') as f:
                f.write(content)
        except FileNotFoundError:
            self.logger.debug('FileNotFoundError Failed to delete file')
            os.makedirs(self.download_path)
            with open(filename, 'a') as f:
                f.write(content)
            self.logger.info('Write to file:%s %s', content, filename)
