import util.versions
import functools
import enum
import sys
import os

MADE_WITH_PYINSTALLER = hasattr(sys, '_MEIPASS')
# TODO: don't make things depend on parent directories.
TOP_DIR = \
    os.path.dirname(sys.executable) \
    if MADE_WITH_PYINSTALLER else \
    os.path.dirname(os.path.dirname(os.path.dirname(__file__)))


class dir_type(enum.Enum):
    RoBLOX = 0
    ASSET = 1
    SSL = 2
    MISC = 3


class bin_subtype(enum.Enum):
    SERVER = 'Server'
    PLAYER = 'Player'
    STUDIO = 'Studio'


DEFAULT_CONFIG_PATH = './GameConfig.toml'


def get_paths(d: dir_type) -> list[str]:
    match (MADE_WITH_PYINSTALLER, d):

        case (True, dir_type.RoBLOX):
            return [TOP_DIR, 'Roblox']
        case (False, dir_type.RoBLOX):
            return [TOP_DIR, 'Roblox']

        case (True, dir_type.ASSET):
            return [TOP_DIR, 'AssetCache']
        case (False, dir_type.ASSET):
            return [TOP_DIR, 'AssetCache']

        # If running from `exe`, stores TLS certiifcates in a temporary directory.
        case (True, dir_type.SSL):
            return [getattr(sys, '_MEIPASS', '')]
        case (False, dir_type.SSL):
            return [TOP_DIR, 'Source', 'ssl']

        case (True, dir_type.MISC):
            return [TOP_DIR]
        case (False, dir_type.MISC):
            return [TOP_DIR]
    return []


@functools.cache
def make_dirs(full_path: str) -> None:
    pieces = []
    head = os.path.abspath(full_path)
    tail = True
    while tail:
        (head, tail) = os.path.split(head)
        pieces.append(head)

    for head in reversed(pieces):
        if not os.path.exists(head):
            os.mkdir(head)


def retr_full_path(d: dir_type, *paths: str) -> str:
    full_path = os.path.join(*get_paths(d), *paths)
    make_dirs(full_path)
    return full_path


def retr_roblox_full_path(version: util.versions.roblox, bin_type: bin_subtype, *paths: str) -> str:
    return retr_full_path(dir_type.RoBLOX, version.name, bin_type.value, *paths)


def retr_config_full_path(path: str = DEFAULT_CONFIG_PATH) -> str:
    if not os.path.isabs(path):
        path = os.path.join(
            retr_full_path(dir_type.MISC),
            path,
        )
    return os.path.normpath(path)
