import enum
import sys


class Lexer:
    def __init__(self, source):
        self.source = source + "\n"
        self.currentChar = ""
        self.currentPosition = -1
        self.nextChar()

    # Goes to the next character
    def nextChar(self):
        self.currentPosition += 1

        if self.currentPosition >= len(self.source) - 1:
            self.currentChar = "\0"
            return

        self.currentChar = self.source[self.currentPosition]

        return self.currentChar

    # Returns the next character without going to the next one
    def peek(self):
        if self.currentPosition >= len(self.source) - 1:
            return "\0"

        return self.source[self.currentPosition + 1]

    # Throws an error message and exits the program when detecting an invalid character
    def abort(self, message):
        sys.exit("Lexing error. " + message)

    # Skips whitespaces (spaces, tabs, newlines or what you define as whitespace)
    def skipWhitespace(self):
        if self.currentChar in " \t\n":
            self.nextChar()

    # Skips comments
    def skipComment(self):
        if self.currentChar == "#":
            while self.currentChar != "\n":
                self.nextChar()

    # Returns the next token
    def getToken(self):
        self.skipWhitespace()
        self.skipComment()

        token = None

        if self.currentChar == "\0":
            token = Token("", TokenType.EOF)
        elif self.currentChar == "+":
            token = Token(self.currentChar, TokenType.SUM)
        elif self.currentChar.isdigit():
            token = Token(self.currentChar, TokenType.NUMBER)
        else:
            self.abort("Unknown character '" + self.currentChar + "'")

        self.nextChar()

        return token


class Token:
    def __init__(self, lexeme, type) -> None:
        self.lexeme = lexeme
        self.type = type


class TokenType(enum.Enum):
    EOF = -1
    NUMBER = 1
    SUM = 202
