import plugins
from plugins import *  # Required to be able to get modules below
hooks = {k: v for m in plugins.__all__ for k, v in getattr(plugins, m).hooks.items()}