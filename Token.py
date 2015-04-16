from TokenType import TokenType


class Token:
    lineNumber = None
    columnNumber = None
    lexeme = None
    data = None
    tokenType = None

    semanticRecord = None

    def __init__(self, inLexeme, inLineNum, inColumnNum, inTokenType):
        self.lexeme = inLexeme
        self.lineNumber = inLineNum
        self.columnNumber = inColumnNum
        self.tokenType = inTokenType

    def getType(self):
        return(self.tokenType)

    def getLexeme(self):
        return(self.lexeme)

    def getLineNumber(self):
        return(self.lineNumber)

    def getColumnNumber(self):
        return(self.columnNumber)

    def printToken(self):
        print(self.lexeme, self.lineNumber, self.columnNumber, self.tokenType)
