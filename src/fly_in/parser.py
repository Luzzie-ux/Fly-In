# Parser and Config class
from collections import Counter
from collections.abc import Generator
from dataclasses import dataclass
from pathlib import Path
from string import whitespace
from typing import ClassVar

from .symbols import RULES, Connection, Hub, MapSymbols, Tokens, WhiteSpaces


@dataclass
class Config:
    mapname: str
    nb_drones: int
    start_hub: Hub
    hubs: list[Hub]
    connections: list[Connection]
    end_hub: Hub


class AnalysisError(Exception):
    def __init__(self, msg: str | None) -> None:
        if not msg:
            msg = "AnalysisError: Unknown Error"
        super().__init__(msg)


class Analyser:
    # properties:
    __files: ClassVar[list[dict[int, list[str]]]] = []
    __maps: ClassVar[list[Config]] = []

    @staticmethod
    def __default(args: list[str] | None) -> list[str]:
        mins = 2
        if not args or len(args) < mins:
            print("[Warn]: No arguments given, defaulting for a demo file")
            folder = Path(__file__).parent
            return [str(file) for file in folder.glob("demo.txt")]
        return args[1:]

    @staticmethod
    def __empty(s: str) -> None:
        if not s.strip(whitespace):
            msg = "[Error]: Invalid Argument, got: ''"
            raise ValueError(msg)
        if not Path(s).stat().st_size:
            msg = f"[Error]: Expected non-empty file, got: {s}"
            raise OSError(msg)

    @classmethod
    def validate(cls, argv: list[str] | None) -> None:
        args: list[str] = cls.__default(argv)

        try:
            for path in args:
                cls.__empty(path)
                cls.__files.append(cls.__lexer(path))
        except (OSError, ValueError) as perr:
            raise AnalysisError(str(perr)) from perr

        cls.__parser()

    @staticmethod
    def __lexer(path: str) -> dict[int, list[str]]:
        def check_dict(d: dict[int, list[str]]) -> None:
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
            return check_counts(d)

        def check_counts(contents: dict[int, list[str]]) -> None:
            counts = Counter(v[0] for v in contents.values() if v)
            for tok, (lo, hi) in RULES.items():
                n = counts[tok]
                if n < lo or (hi is not None and n > hi):
                    expected = (
                        f"exactly {lo}" if lo == hi
                        else f"at least {lo}" if hi is None
                        else f"between {lo} and {hi}"
                    )
                    msg = f"Expected {expected} '{tok}' token(s), got {n}"
                    raise ValueError(msg)

        d: dict[int, list[str]] = {}
        with Path(path).open(mode="r", encoding="utf-8") as file:
            d[-1] = [file.name]
            for index, line in enumerate(file.readlines()):
                if line[0] in WhiteSpaces:
                    continue
                d[index] = line.split(" ")
            d[index + 1] = [Tokens["terminator"]]
        check_dict(d)

        return d

    @classmethod
    def __parser(cls) -> None:
        for file in cls.files():
            name = file[-1][0]
            print(f"Inspecting {name}")
            for k, v in file.items():
                if k == -1:
                    continue
                print(k, v)

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
