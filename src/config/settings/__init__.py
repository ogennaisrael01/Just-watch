from .prod import ProdSettings
from .dev import DevelopmentSetting
from .base import BaseSetting


dev_settings = DevelopmentSetting()
prod_settings = ProdSettings()
base_setting = BaseSetting()

DEFAULT_PAGE=1


__all__ = [
    "DEFAULT_PAGE",
    "dev_settings",
    "prod_settings",
    "base_setting",
]