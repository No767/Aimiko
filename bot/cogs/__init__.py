from pkgutil import iter_modules
from typing import Literal, NamedTuple


class VersionInfo(NamedTuple):
    major: int
    minor: int
    micro: int
    releaselevel: Literal["alpha", "beta", "candidate", "final"]
    serial: int


EXTENSIONS = [module.name for module in iter_modules(__path__, f"{__package__}.")]

VERSION: VersionInfo = VersionInfo(
    major=0, minor=1, micro=0, releaselevel="alpha", serial=0
)
