__title__ = "disco.oauth2"
__author__ = "martimartins"
__author_email__ = "martim13artins13@gmail.com"
__license__ = "MIT"
__copyright__ = "Copyright 2022-present Martim Martins"
__version__ = "1.2a"

from typing import Literal, NamedTuple

from .client import *
from .errors import *
from .flags import *
from .guild import *
from .http import *
from .token import *
from .user import *
from .connection import *
from .integration import *
from .member import *
from .token import *
from .appinfo import *

_VersionInfo = NamedTuple(
    "_VersionInfo",
    major=int,
    minor=int,
    micro=int,
    releaselevel=Literal["alpha", "beta", "candidate", "final"],
    serial=int,
)

version_info = _VersionInfo(major=1, minor=2, micro=0, releaselevel="alpha", serial=0)
