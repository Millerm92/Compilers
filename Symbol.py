# SYMBOL


class Symbol:
    lexeme = None
    _type = None
    kind = None
    offset = None
    label = None

    def __init__(self, inID, inType, inKind, inOffSet, inLabel):
        self.lexeme = inID
        self._type = inType
        self.kind = inKind
        self.offset = inOffSet + 1

        self.label = inLabel

    def getOffset(self):
        return self.offset

    def getLexeme(self):
        return self.lexeme

    def getKind(self):
        return self.kind

    def setType(self, inType):
        self._type = inType

    def getType(self):
        return self._type

    def printSymbol(self):
        print(self.lexeme, self._type, self.kind, self.offset, self.label)
