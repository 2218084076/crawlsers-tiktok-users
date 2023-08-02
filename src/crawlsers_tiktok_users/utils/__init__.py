"""BaseUtils"""
import asyncio

from crawlerstack_spiderkeeper_sdk.exceptions import SpiderkeeperSdkException

from crawler_customsdata.config import settings


class BaseUtils:  # pylint: disable=too-few-public-methods
    """BaseUtils"""

    def __init__(self):
        self.export_columns = [
            'Month',
            'Code',
            'CodeDesc',
            'CountryCode',
            'Country',
            'CustomsCode',
            'CustomsRegime',
            'ProvinceCode',
            'Province',
            'Qty1',
            'Qty1Unit',
            'Qty2',
            'Qty2Unit',
            'ValueUSD',
        ]
        self.columns = [
            'Code',
            'CodeDesc',
            'CountryCode',
            'Country',
            'CustomsCode',
            'CustomsRegime',
            'ProvinceCode',
            'Province',
            'Qty1',
            'Qty1Unit',
            'Qty2',
            'Qty2Unit',
            'ValueUSD',
        ]


class SingletonMeta(type):
    """
    单例元类

    example:
        class Foo(metaclass=SingletonMeta):...
    """
    __instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls.__instances:
            instance = super().__call__(*args, **kwargs)
            cls.__instances[cls] = instance
        return cls.__instances[cls]


class SDK(metaclass=SingletonMeta):
    """SDK"""

    def __init__(self):

        self.metrics_task = None

    @property
    def repeater(self):
        """
        sdk
        :return:
        """
        try:
            return SpiderkeeperSDK(
                task_name=settings.TASK_NAME,
                data_url=settings.DATA_URL,
                log_url=settings.LOG_URL,
                metrics_url=settings.METRICS_URL,
                storage_enabled=state_check(settings.STORAGE_ENABLE),
                snapshot_enabled=state_check(settings.SNAPSHOT_ENABLE),
            )
        except Exception as ex:
            raise SpiderkeeperSdkException('Initialization failure') from ex

    def init_metrics_collector_task(self):
        """init metrics collector task"""
        self.metrics_task = asyncio.create_task(self.repeater.send_metrics())


class SpiderkeeperSDK:
    """repeater"""
    MAX_RETRY = 1
    metrics_data = {}

    def __init__(
            self,
            task_name: str,
            data_url: str,
            log_url: str,
            metrics_url: str,
            storage_enabled=False,
            snapshot_enabled=False
    ):
        self.metrics_task = None
        self.task_name: str = task_name
        self.log_url: str = log_url
        self.data_url: str = data_url
        self.metrics_url: str = metrics_url
        self.storage_enabled = storage_enabled
        self.snapshot_enabled = snapshot_enabled
        self._should_exit: bool = False

    async def send_data(self, data: dict, data_type: str = 'data'):
        """
        发送数据

        接口接收到的数据参数中fields与datas长度应保持一致
        :param data_type: 选择传入数据保存方式 `data`表示需要写入数据库的数据 `snapshot`表示需要保存为快照的文件数据
        :param data:
        :return:
        """
        if data_type == 'data':
            if self.storage_enabled:
                data.update({'snapshot_enabled': False})
            else:
                return 'Storage not enabled'
        elif data_type == 'snapshot':
            if self.snapshot_enabled:
                data.update({'snapshot_enabled': True})
            else:
                return 'Snapshot not enabled'

    async def send_log(self, log: str):
        """
        send_log

        上传必要的 log 日志信息
        :param log:
        :return:
        """
        data = {
            'task_name': self.task_name,
            'data': [log]
        }
        print(data)

    async def send_metrics(self):
        """
        监控指标上传

        由 SDK 程序自行获取所需指标，并将时间周期内指标上传
        :return:
        """
        print('send_metrics')


def state_check(content) -> bool:
    """
    Enable
    :param content:
    :return:
    """
    if isinstance(content, str):
        content = content.lower()
    if content == 'true' or content is True:
        return True
    return False
