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

    def blockDec(self, inSize):
        self.outputFile.write("ADD SP #%d SP\n" % (inSize + 1))

    def pushToStack(self, lexeme, sTable):
        offset = sTable.getOffset(lexeme)
        if offset is not None:
            self.outputFile.write("PUSH %d(D0)\n" % offset)
        else:
            print("ERROR: %s is undeclared" % (lexeme))

    def pushLitToStack(self, inLit):
        self.outputFile.write("PUSH #%s\n" % str(inLit))

    def assignment(self, res, expType, offset):
        if res == "MP_FIXED":
            res = "MP_FLOAT"
        if expType == "MP_FIXED":
            expType = "MP_FLOAT"

        if res == expType:
            pass
        elif res == "MP_FLOAT" and expType == "MP_INTEGER":
            self.outputFile.write("CASTSF\n")
        elif res == "MP_INTEGER" and expType == "MP_FLOAT":
            self.outputFile.write("CASTSI\n")
        else:
            print("ERROR: Assignment of conflicting types")

        self.outputFile.write("POP %d(D0)\n" % offset)

    def expression(self, term1, term2, operator):
        if(term1 == "MP_FIXED"):
            term1 = "MP_FLOAT"
        if (term2 == "MP_FIXED"):
            term2 = "MP_FLOAT"

        if term1 == term2:
            pass
        elif term1 == "MP_INTEGER" and term2 == "MP_FLOAT":
            self.outputFile.write("CASTSI\n")
        elif term1 == "MP_FLOAT" and term2:
            self.outputFile.write("CASTF\n")
        else:
            print("ERROR: Incompatable Types")

        if (term1 == "MP_FLOAT"):
            operator += "F"

        self.outputFile.write("%s\n" % (operator))

    def readStatement(self, inLexeme, curTable):
        offset = curTable.getOffset(inLexeme)
        _type = curTable.getType(inLexeme)

        if _type == TokenType.MP_FLOAT or _type == TokenType.MP_FIXED:
            self.outputFile.write("RDF %d(D0)\n" % (offset))
        else:
            self.outputFile.write("RD %d(D0)\n" % (offset))

    def writeStatement(self, inWriteLn):
        if inWriteLn:
            self.outputFile.write("WRTLNS\n")
        else:
            self.outputFile.write("WRTS\n")
