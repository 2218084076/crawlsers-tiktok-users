"""download file"""
import csv
import datetime
import logging
import os
import shutil
from pathlib import Path

from crawler_customsdata.config import settings


class DownloadFile:
    """Download File"""

    download_path = settings.DOWNLOAD_PATH

    def __init__(self, date: str):
        self.file_path = None
        self.now_datetime = datetime.datetime.now()
        self.date = date
        self.logger = logging.getLogger(f'{__name__}.{self.__class__.__name__}')
        self.trash_path = settings.TRASH_PATH

    @property
    def get_file(self) -> list:
        """
        get file
        :return:
        """
        try:
            files = Path(f'{self.download_path}/{self.date}').iterdir()
            download_file_list = []
            for file in files:
                if file.is_file():
                    download_file_list.append(file)
            return download_file_list
        except FileNotFoundError:
            self.logger.debug('File list does not exist')
            return []

    def read_file(self, file: Path):
        """
        read file
        :param file:
        :return:
        """
        info_list = []
        self.logger.debug('Read %s', file)
        with open(file, encoding='GBK') as obj:
            try:
                data = csv.DictReader(obj)
                for row in data:
                    info_list.append(row)
            except Exception as exc:
                print(exc, file)

        return info_list

    def move_files(self, file):
        """
        move_files
        :param file:
        :return:
        """
        try:
            self.logger.debug('Move Files %s', file)
            shutil.move(Path(file), Path(self.trash_path) / self.date / file.name)
        except FileNotFoundError:
            os.makedirs(Path(self.trash_path) / self.date, exist_ok=True)
            self.logger.debug('FileNotFoundError Failed to delete file')
            shutil.move(Path(file), Path(self.trash_path) / self.date / file.name)
            self.logger.debug('Move Files %s', file)
