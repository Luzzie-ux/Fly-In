from sys import argv, exit
from fly_in import Parser

input = Parser(argv)
if input < 2:
    print("ERROR")
    exit(1)
input()
