import logging
from pathlib import Path
from datetime import datetime
from typing import TextIO
from itertools import count
from PIL import Image, ImageTk

from constants import ASSETS_PATH, PATH, FILENAME_PREFIX_FORMAT
from exceptions import ImageNotFound


log = logging.getLogger(__name__)


def validate_dirs(dirs) -> None:
    """Creates app directories if they don't already exist."""
    log.info('Validating app dirs')
    # create directories in the appdata dir
    Path(dirs.user_config_dir).mkdir(parents=True, exist_ok=True)
    Path(dirs.user_log_dir).mkdir(parents=True, exist_ok=True)
    # create directories with the project files
    for folder_name in ('output', 'assets', 'theme'):
        Path(
            f'{PATH}\{folder_name}'
        ).mkdir(parents=True, exist_ok=True)

def open_new_file(dir:str, prefix:str='', ext:str='txt') -> TextIO:
    """Create a new file with a unique filename"""
    timestamp = datetime.now().strftime(FILENAME_PREFIX_FORMAT)
    filenames = (
            f'{prefix}_{timestamp}.txt' if i == 0 else \
            f'{prefix}_{timestamp}_{i}.{ext}' for i in count()
        )
    for filename in filenames:
        try:
            path = f'{dir}/{filename}'
            log.debug(f'Creating file at {path}')
            return (Path(path).open('x', encoding='utf-8'))
        except FileExistsError:
            continue

def image(filename:str, size:tuple[int, int]) -> ImageTk.PhotoImage:
    """returns PhotoImage object obtained from file path"""
    fp = f'{ASSETS_PATH}\{filename}'
    if not Path(fp).exists():
        log.error(f'could not find image at fp: {fp}')
        raise ImageNotFound
    im = Image.open(fp)
    im = im.resize(size, Image.ANTIALIAS)
    return ImageTk.PhotoImage(im)

def up_list(_list:list[str]) -> list[str]:
    """
        Returns a duplicate of the entered list except all contained
        strings are uppercase.
    """
    try:
        new_list = [item.upper() for item in _list.copy()]
        return new_list
    except TypeError:
        # Is this pythonic?
        raise TypeError('Items in list must be of type str')