from enum import Enum, auto

Name = str
Point = tuple[int, int]
Drones = int
Metadata = tuple[dict[str, str | int]] | dict[str, str | int] | None
Hub = tuple[Name, Point, Metadata]
Connection = tuple[dict[Name, Name], Metadata]

class TokenTypes(Enum):
    COMMENT = auto()
    NBR_DRONES = auto()
    START = auto()
    HUB = auto()
    END = auto()
    CONNECTION = auto()

Token = dict[str, TokenTypes]

TOKENS: Token = {
        '#': TokenTypes.COMMENT,
        'nbr_drones:': TokenTypes.NBR_DRONES,
        'start_hub:': TokenTypes.START,
        'hub:' : TokenTypes.HUB,
        'end_hub' : TokenTypes.END,
        'connection' : TokenTypes.CONNECTION
        }
