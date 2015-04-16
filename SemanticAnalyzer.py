# Semantic Analyzer
import SymbolTable
import Symbol
from TokenType import TokenType


class SemanticAnalyzer:
    outputFile = None

    def __init__(self):
        self.outputFile = open('output.txt', 'w')
        self.endString = ""

    def write(self, inString):
        self.outputFile.write(inString)

    def progDec(self, inNest, inSize, inLabel):
        self.outputFile.write("ADD SP #" + inSize + " SP\n")

    def readStatement(self, inLexeme, curTable):
        offset = curTable.getOffset(inLexeme)
        _type = curTable.getType(inLexeme)

        if _type == TokenType.MP_FLOAT or _type == TokenType.MP_FIXED:
            self.outputFile.write("RDF @" + offset[0] + "(D" + offset[1] + ")\n")
        else:
            self.outputFile.write("RD @" + offset[0] + "(D" + offset[1] + ")\n")

    def writeStatement(self, inWriteLn):
        if inWriteLn:
            self.outputFile.write("WRTLNS\n")
        else:
            self.outputFile.write("WRTS\n")
