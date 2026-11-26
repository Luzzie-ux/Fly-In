# Parser and Config class
from collections.abc import Generator
from dataclasses import dataclass
from pathlib import Path
from string import whitespace
from typing import ClassVar

from .symbols import Connection, Hub, MapSymbols, Tokens, WhiteSpaces


@dataclass
class Config:
    mapname: str
    nb_drones: int
    start_hub: Hub
    hubs: list[Hub]
    connections: list[Connection]
    end_hub: Hub


class ParserError(Exception):
    def __init__(self, msg: str | None) -> None:
        if not msg:
            msg = "ParserError: Unknown Error"
        super().__init__(msg)


class Parser:
    # properties:
    __files: ClassVar[list[dict[int, list[str]]]] = []
    __maps: ClassVar[list[Config]] = []

    @staticmethod
    def __empty(s: str) -> None:
        if not s.strip(whitespace):
            msg = "[Error]: Invalid Argument, got: ''"
            raise ValueError(msg)
        if not Path(s).stat().st_size:
            msg = f"[Error]: Expected non-empty file, got: {s}"
            raise OSError(msg)

    @classmethod
    def validate(cls, args: list[str]) -> None:
        min_arg = 2
        if len(args) < min_arg:
            msg = f"Usage: {args[0]} <args>"
            raise ParserError(msg)

        try:
            for path in args[1:]:
                cls.__empty(path)
                cls.__lexer(path)
        except (OSError, ValueError) as perr:
            raise ParserError(str(perr)) from perr

    @classmethod
    def __lexer(cls, path: str) -> None:
        d: dict[int, list[str]] = {}
        with Path(path).open(mode="r", encoding="utf-8") as file:
            d[-1] = [file.name]
            for index, line in enumerate(file.readlines()):
                if line[0] in WhiteSpaces:
                    continue
                d[index] = line.split(" ")
            d[index + 1] = [Tokens["terminator"]]

        contents = {
            k: v for k, v in d.items()
            if k != -1 and v != [Tokens["terminator"]]
        }

        if not contents:
            msg = f"Empty file {d[-1][0]}"
            raise ValueError(msg)

        for k, v in contents.items():
            if v[0] not in MapSymbols:
                msg = f"Invalid Token found in line {k}, got: {v[0]}"
                raise ValueError(msg)

        cls.__files.append(d)

    @classmethod
    def __syntax(cls) -> None:
        pass

    @classmethod
    def __semantics(cls) -> None:
        pass

    @classmethod
    def files(cls) -> Generator[dict[int, list[str]]]:
        yield from cls.__files

    @classmethod
    def maps(cls) -> Generator[Config]:
        yield from cls.__maps

    @classmethod
    def log(cls) -> None:
        for file in cls.files():
            print(f"\n=== {file[-1][0]}")
            for k, v in file.items():
                if k != -1 and v[0] != Tokens["terminator"]:
                    print(f"{k}: {v}")
        print("=" * 50)
