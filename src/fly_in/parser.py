# Parser and Config class
from string import whitespace
from collections.abc import Generator
from os import stat
from .symbols import (Hub, Connection, Tokens, WhiteSpaces, MapSymbols)

class Config:
    mapname: str
    nb_drones: int
    start_hub: Hub
    hubs: list[Hub]
    connections: list[Connection]
    end_hub: Hub

    def __init__(self) -> None: ...

class ParserError(Exception):
    def __init__(self, msg: str | None) -> None:
        if not msg:
            msg = "ParserError: Unknown Error"
        super().__init__(msg)

class Parser:
    # properties:
    __files: list[dict[int, list[str]]] = []
    __config: Config = Config()

    # constructors
    def __new__(cls) -> None:
       raise TypeError("Parser Class cannot be constructed")

    @classmethod
    def getConfig(cls) -> Config:
        return cls.__config

    @classmethod
    def getFile(cls) -> Generator[dict[int, list[str]]]:
        yield from cls.__files

    @classmethod
    def logInput(cls) -> None:
        for file in cls.getFile():
            print(f"\n=== {file[-1][0]}")
            for k, v in file.items():
                if k != -1 and v[0] != Tokens['terminator']:
                    print(f"{k}: {v}")
        print("="*50)

    @classmethod
    def validate(cls, args: list[str]) -> None:
        def check(args: list[str]) -> None:
            size = len(args)
            try:
                if size < 2:
                    msg = f"Fly-In requires at least 2 arguments: got {size}"
                    raise ValueError(msg)
            except ValueError as valErr:
                raise ParserError(str(valErr)) from valErr

        check(args)
        for path in args[1: ]:
            try:
                if not path.strip(whitespace) or not stat(path).st_size:
                    raise ValueError(f"Invalid Argument, got: {path}")

                cls.__lexer(path)
            except (FileNotFoundError, OSError, ValueError) as perr:
                raise ParserError(str(perr)) from perr

    @classmethod
    def __lexer(cls, path: str) -> None:
        d: dict[int, list[str]] = {}
        with open(path) as file:
            d[-1] = [file.name]
            for index, line in enumerate(file.readlines()):
                if line[0] in WhiteSpaces:
                    continue
                d[index] = line.split(' ')
            d[index+1] = [Tokens['terminator']]

        contents = {
            k:v for k,v in d.items()
            if k != -1 and v != [Tokens['terminator']]
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
    def __syntaxer(cls) -> None: ...
    @classmethod
    def __parser(cls) -> None: ...
