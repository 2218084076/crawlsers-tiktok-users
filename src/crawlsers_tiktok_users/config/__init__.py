"""
Configuration center.
Use https://www.dynaconf.com/
"""""
import sys
from pathlib import Path

from dynaconf import Dynaconf

_base_dir = Path(__file__).parent.parent.parent

_settings_files = [
    Path(__file__).parent / 'settings.yml',
]

_external_files = [
    Path(sys.prefix, 'etc', 'crawlsers', 'tiktok_users', 'settings.yml')
]
settings = Dynaconf(
    envvar_prefix=False,
    # 配置初始化时需要禁用前缀以便采集平台环境变量注入
    settings_files=_settings_files,
    load_dotenv=True,
    lowercase_read=False,
    includes=_external_files,
    basedir=_base_dir,
)
