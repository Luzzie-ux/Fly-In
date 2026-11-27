Point = tuple[int, int]
Metadata = dict[str, str]
Hub = tuple[str, Point, Metadata]
Connection = tuple[dict[str, str], Metadata]

MIN = 2

Tokens: dict[str, str] = {
        "comment": "#",
        "space": " ",
        "endl": "\n",
        "tab": "\t",
        "drones": "nb_drones:",
        "start": "start_hub:",
        "hub": "hub:",
        "end": "end_hub:",
        "connection": "connection:",
        "terminator": "\0"
    }

WhiteSpaces: tuple[str, ...] = (
        Tokens["space"],
        Tokens["tab"],
        Tokens["endl"],
        Tokens["comment"]
    )

MapSymbols: tuple[str, ...] = (
        Tokens["drones"],
        Tokens["start"],
        Tokens["hub"],
        Tokens["end"],
        Tokens["connection"]
    )

RULES: dict[str, tuple[int, int | None]] = {
    Tokens["drones"]: (1, 1),
    Tokens["start"]: (1, 1),
    Tokens["end"]: (1, 1),
    Tokens["hub"]: (1, None),
    Tokens["connection"]: (2, None),
}

HUBS: set[str] = {Tokens["start"], Tokens["hub"], Tokens["end"]}
