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
        while self.currentChar in " \t\n":
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
        elif self.currentChar == "=":
            token = Token("=", TokenType.EQUAL)
        elif self.currentChar == "+":
            token = Token(self.currentChar, TokenType.SUM)
        elif self.currentChar == "-":
            token = Token(self.currentChar, TokenType.SUBTRACTION)
        elif self.currentChar == "*":
            token = Token(self.currentChar, TokenType.MULTIPLICATION)
        elif self.currentChar == "/":
            token = Token(self.currentChar, TokenType.DIVISION)
        elif self.currentChar == ">":
            if self.peek() == "=":
                self.nextChar()
                token = Token(">=", TokenType.GREATER_THAN_OR_EQUAL)
            else:
                token = Token(">", TokenType.GREATER_THAN)
        elif self.currentChar == "<":
            if self.peek() == "=":
                self.nextChar()
                token = Token("<=", TokenType.LESS_THAN_OR_EQUAL)
            else:
                token = Token("<", TokenType.LESS_THAN)
        elif self.currentChar == "!":
            if self.peek() == "=":
                self.nextChar()
                token = Token("!=", TokenType.NOT_EQUAL)
            else:
                token = Token("!", TokenType.NOT)
        elif self.currentChar.isdigit():
            initialPosition = self.currentPosition

            while self.peek() != "\0" and self.peek().isdigit():
                self.nextChar()

            lexeme = self.source[initialPosition : self.currentPosition + 1]
            token = Token(lexeme, TokenType.NUMBER)
        elif self.currentChar.isalpha():
            initialPosition = self.currentPosition

            while self.peek() != "\0" and self.peek().isalnum():
                self.nextChar()

            lexeme = self.source[initialPosition : self.currentPosition + 1]

            type = Token.check_reserved_keywords(lexeme)

            if type == None:
                token = Token(lexeme, TokenType.IDENTIFIER)
            else:
                token = Token(lexeme, type)
        else:
            self.abort("Unknown character '" + self.currentChar + "'")

        self.nextChar()

        return token


class Token:
    def __init__(self, lexeme, type) -> None:
        self.lexeme = lexeme
        self.type = type

    def check_reserved_keywords(lexeme):
        for type in TokenType:
            if type.name == lexeme and type.value >= 100 and type.value < 200:
                return type


class TokenType(enum.Enum):
    EOF = -1
    NUMBER = 1
    IDENTIFIER = 2

    # Reserved keywords
    IF = 101
    THEN = 102
    PRINT = 103
    ENDIF = 104

    # Operators
    EQUAL = 202
    SUM = 203
    SUBTRACTION = 204
    MULTIPLICATION = 205
    DIVISION = 206
    GREATER_THAN = 207
    GREATER_THAN_OR_EQUAL = 208
    LESS_THAN = 209
    LESS_THAN_OR_EQUAL = 210
    NOT = 211
    NOT_EQUAL = 212
