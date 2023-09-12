from enum import Enum

YOUTUBE_PREFIX = 'https://www.youtube.com/watch?v='
YOUTUBE_LINK_PATTERN = r'(?:(?:https?:\/\/)?(?:www\.)?(?:youtube\.com|youtu\.be)\/(?:watch\?\S*v=)?|^(?!.*watch\?\S*v=))(.*?)($|\s)'


class Emojis(Enum):
    EYE = '\U0001F441'
    MAN = '\U0001F464'
    CLOCK_1 = '\U0001F570'
    CAMERA = '\U0001F4FD'
    INBOX_TRAY = '\U0001F4E5'
    CALENDAR = '\U0001F4C5'
    DONE = '\U00002705'
    IN_PROGRESS = '\U0000231B'
    CANCELED = '\U0000274C'
    SONG = '\U0001F3B5'
    DURATION = '\U0001F551'
    STONE_FACE = '\U0001F5FF'
