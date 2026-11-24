# Parser and Config class

from .maptypes import (Hub, Connection, Metadata, Token, TOKENS)

class Config:
    start_hub: Hub
    hubs: list[Hub]
    connections: list[Connection]
    end_hub: Hub

    def __init__(self) -> None:
        return

class Parser:
    # constructor
    def __init__(self, args: list[str]) -> None:
        self.__args = args
        self.__size = len(args)
        self.__config = Config()
        self.__tokens = list[Token]

    # operators:
    def __call__(self) -> Config:
        return self.__config
    def __lt__(self, nbr: int) -> bool:
        return self.__size < nbr

    # methods:
    def __preprocessing(self): ...
    def __parsing(self): ...
    def __checking(self): ...
    def __lexing(self): ... 
