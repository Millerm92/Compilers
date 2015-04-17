# Symbol Table


class SymbolTable:
    name = ""
    nestLevel = 0
    label = 0

    tuples = []
    parent = None

    def __init__(self, inName, inLabel, inParent):
        self.name = inName
        self.label = inLabel
        self.parent = inParent

        self.tuples = []

    def insert(self, inSymbol):
        self.tuples.append(inSymbol)

    def getName(self):
        return self.name

    def getTuples(self):
        return self.tuples

    def getNumTuples(self):
        return len(self.tuples)

    def getLabel(self):
        return self.label

    def setParent(self, inParent):
        self.parent = inParent

    def getParent(self):
        return self.parent

    def getOffset(self, inLexeme):
        for s in self.tuples:
            if (s.getLexeme() == inLexeme):
                ret = [s.getOffset, self.nestLevel]
                return ret

    def getType(self, inLexeme):
        for s in self.tuples:
            if (s.getLexeme() == inLexeme):
                return s.getType()

    def getKind(self, inLexeme):
        for s in self.tuples:
            if (s.getLexeme() == inLexeme):
                return s.getKind()

    def getSymbol(self, inLexeme):
        for s in self.tuples:
            if (s.getLexeme() == inLexeme):
                return s

    def printSymbolTable(self):
        print("\n%s, %d" % (self.name, self.nestLevel))
        for t in self.tuples:
            t.printSymbol()
