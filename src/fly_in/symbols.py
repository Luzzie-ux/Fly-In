Name = str
Value = str | int
Point = tuple[int, int]
Drones = int
Metadata = tuple[dict[Name, Value]] | dict[Name, Value] | None
Hub = tuple[Name, Point, Metadata]
Connection = tuple[dict[Name, Name], Metadata]

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
