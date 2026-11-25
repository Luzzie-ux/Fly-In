# Parser and Config class
from string import whitespace
from sys import stderr, argv
from os import stat
from .symbols import (Hub, Connection, Metadata, Tokens)

class Config:
    mapname: str
    nb_drones: int
    start_hub: Hub
    hubs: list[Hub]
    connections: list[Connection]
    end_hub: Hub

    def __init__(self) -> None: ...

class ParserError(Exception): ...

class Parser:
    # properties:
    __tokens: list[tuple[int, list[str]]]
    __config: Config
    __filenames: list[str]

    # constructors
    def __new__(cls) -> None:
        cls.__tokens = []
        cls.__config = Config()
        cls.__filenames = []
    
    @classmethod
    def validate(cls, args: list[str] = argv) -> None:
        def check(args: list[str]) -> None:
            size = len(args)
            try:
                if size < 2:
                    msg = f"Fly-In requires at least 2 arguments: got {size}"
                    raise ValueError(msg)
            except ValueError as e:
                print(str(e), file=stderr)
                raise ParserError
        check(args)
        for i, path in enumerate(args[1: ]):
            try:
                if not path.strip(whitespace):
                    raise ValueError(f"Empty Argument Nº: {i}")
                if not stat(path).st_size:
                    raise ValueError(f"Empty File: {path}")
                cls.__filenames.append(path)
                cls.__lexer(path)
            except (FileNotFoundError, PermissionError,
                    IsADirectoryError, OSError) as ioErr:
                print(f"{ioErr}", file=stderr)
                raise ParserError
            except ValueError as valErr:
                print(f"[Error]: {valErr}", file=stderr)
                raise ParserError

    @classmethod
    def __lexer(cls, path: str) -> None:
        def isIgnorable(s: str) -> bool:
            return s in (Tokens['space'], Tokens['endl'],
                         Tokens['tab'], Tokens['comment'])
        name: str = ''
        with open(path) as file:
            name = file.name
            for index, line in enumerate(file.readlines()):
                if isIgnorable(line[0]):
                    continue
                cls.__tokens.append((index, line.split()))
            cls.__tokens.append((index+1, [Tokens['terminator']]))
        tokens = cls.__tokens
        for (_, ts) in tokens:
            if len(ts) == 1:
                raise ValueError(f'Empty File: {name}')

    @classmethod
    def __syntaxing(cls):
        ...
    @classmethod
    def __parsing(cls): ...
    @classmethod
    def getTokens(cls) -> list[tuple[int, list[str]]]: return cls.__tokens
    @classmethod
    def getConfig(cls) -> Config: return cls.__config
