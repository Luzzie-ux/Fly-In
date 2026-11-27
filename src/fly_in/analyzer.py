# Parser and Config class
from collections import Counter, abc
from pathlib import Path
from string import whitespace
from typing import ClassVar

from .symbols import Connection, Hub, MapSymbols, Tokens, WhiteSpaces
from .symbols import MIN, RULES, HUBS


class Config:
    mapname: str
    nb_drones: int
    start_hub: Hub
    hubs: list[Hub]
    connections: list[Connection]
    end_hub: Hub

    def __init__(self) -> None: ...


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
        if not args or len(args) < MIN:
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
                cls.__lexer(path)
        except (OSError, ValueError) as perr:
            raise AnalysisError(str(perr)) from perr

        cls.__parser()

    @staticmethod
    def __check_dict(d: dict[int, list[str]]) -> None:
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

        counts = Counter(v[0] for v in contents.values() if v)
        for tok, (lo, hi) in RULES.items():
            n = counts[tok]
            if n < lo or (hi is not None and n > hi):
                expected = (
                    f"exactly {lo}" if lo == hi
                    else f"at least {lo}" if hi is None
                    else f"between {lo} and {hi}"
                )
                msg = f"[Error]: Expected {expected} '{tok}' token(s), got {n}"
                raise ValueError(msg)

    @classmethod
    def __lexer(cls, path: str) -> None:
        d: dict[int, list[str]] = {}

        with Path(path).open(mode="r", encoding="utf-8") as file:
            d[-1] = [file.name]
            for index, line in enumerate(file.readlines()):
                if line[0] in WhiteSpaces:
                    continue
                if line.split(" ") == [line]:
                    msg = f"[Error]: on line no.{index}, got: {line}"
                    raise ValueError(msg)
                d[index] = line.split(" ")
            d[index + 1] = [Tokens["terminator"]]

        cls.__check_dict(d)
        cls.__files.append(d)

    @staticmethod
    def __check_tokens(kind: str, tokens: list[str]) -> None:
        if kind == Tokens["drones"]:
            pass
        elif kind in HUBS:
            pass
        elif kind == Tokens["contents"]:
            pass

    @classmethod
    def __parser(cls) -> None:
        for file in cls.__files:
            config: Config = Config()
            try:
                config.mapname = file[-1][0]
                for v in file.values():
                    cls.__check_tokens(v[0], v[1:])

            except ValueError as e:
                raise AnalysisError(str(e)) from e
            cls.__maps.append(config)

    @classmethod
    def __semantics(cls) -> None:
        pass

    @classmethod
    def files(cls) -> abc.Generator[dict[int, list[str]]]:
        yield from cls.__files

    @classmethod
    def maps(cls) -> abc.Generator[Config]:
        yield from cls.__maps

    @classmethod
    def log(cls) -> None:
        for file in cls.files():
            print(f"\nInspecting {file[-1][0]}")
            for k, v in file.items():
                if k != -1 and v[0] != Tokens["terminator"]:
                    print(f"{k}: {v}")
        print("=" * 50)
