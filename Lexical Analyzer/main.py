from lexer import *


def simple_lexer(source):
    for c in source:
        if c.isdigit():
            print(f"NUMBER: {c}")
        elif c == "+":
            print(f"OPERATOR: {c}")
        else:
            print("ERROR: Character not recognized")


def main():
    # simple_source = "2+3+4+5+6"
    # simple_lexer(simple_source)

    source = "2+ 3+ 4+ 5+ 6 "

    lexer = Lexer(source)
    token = lexer.getToken()
    while token.type != TokenType.EOF:
        print(str(token.type) + " (" + token.lexeme + ")")
        token = lexer.getToken()


main()
