# PARSER
import Token
import SemanticAnalyzer
import SymbolTable
import Symbol
from TokenType import TokenType


class Parser:
    tokens = []
    lookAhead = None
    p = 0

    curTable = None
    nestingLevel = None
    label = 0

    semanticAnalyzer = None

    idenName = None
    idenKind = None
    idenType = None
    idenMode = None

    def __init__(self):
        self.tokens = []
        self.lookAhead = None
        self.p = 0

        self.curTable = None
        self.nestingLevel = 0
        self.label = 0

        self.semanticAnalyzer = SemanticAnalyzer.SemanticAnalyzer()

        self.idenName = None
        self.idenKind = None
        self.idenType = None
        self.idenMode = ""
        self.listOfParams = None

    def addToken(self, inToken):
        self.tokens.append(inToken)

    def printTokens(self):
        for t in self.tokens:
            t.printToken()

    def checkGrammar(self):
        for t in self.tokens:
            t.printToken()

        self.lookAhead = self.tokens[self.p]
        self.systemGoal()
        self.semanticAnalyzer.write("HLT\n")
        return

    def systemGoal(self):
        print("System Goal")
    # program - 1
        if (self.lookAhead.getType() == TokenType.MP_PROGRAM):
            self.program()
            self.match(TokenType.MP_EOF)
        else:
            self.error()
        return

    def program(self):
        print("Program")
        # program - 2
        if (self.lookAhead.getType() == TokenType.MP_PROGRAM):
            self.programHeading()
            self.match(TokenType.MP_SCOLON)
            self.block(True)
            self.match(TokenType.MP_PERIOD)
        else:
            self.error()
        return

    def programHeading(self):
        print("Program Heading")
        # program - 3
        if (self.lookAhead.getType() == TokenType.MP_PROGRAM):
            self.match(TokenType.MP_PROGRAM)
            self.label += 1
            self.curTable = SymbolTable.SymbolTable(self.tokens[self.p].getLexeme(), self.label, None)
            self.programIdentifier()
            self.semanticAnalyzer.write("PUSH D0\n")
            self.semanticAnalyzer.write("MOV SP D0\n")

        else:
            self.error()
        return

    def block(self, inBool):
        print("Block")
        l1 = [TokenType.MP_BEGIN, TokenType.MP_FUNCTION, TokenType.MP_PROCEDURE, TokenType.MP_VAR]
        # begin, function, procedure, var - 4
        if (self.lookAhead.getType() in l1):
            self.variableDeclarationPart()
            self.procedureAndFunctionDeclarationPart()
            self.semanticAnalyzer.blockDec(len(self.curTable.getTuples()))
            self.statementPart()
            self.curTable.printSymbolTable()
            self.curTable = self.curTable.getParent()

        else:
            self.error()
        return

    def variableDeclarationPart(self):
        print("Variable Declaration Part")
        l1 = [TokenType.MP_BEGIN, TokenType.MP_FUNCTION, TokenType.MP_PROCEDURE]
        # var - 5
        if (self.lookAhead.getType() == TokenType.MP_VAR):
            self.idenKind = "var"
            self.match(TokenType.MP_VAR)
            self.variableDeclaration()
            self.match(TokenType.MP_SCOLON)
            self.variableDeclarationTail()

        # begin, function, procedure - 6
        elif (self.lookAhead.getType() in l1):
            return
        else:
            self.error()
        return

    def variableDeclarationTail(self):
        print("Variable Declaration Tail")
        l1 = [TokenType.MP_BEGIN, TokenType.MP_FUNCTION, TokenType.MP_PROCEDURE]
        # id - 7
        if (self.lookAhead.getType() == TokenType.MP_IDENTIFIER):
            self.variableDeclaration()
            self.match(TokenType.MP_SCOLON)
            self.variableDeclarationTail()
        # begin, function, procedure - 8
        elif (self.lookAhead.getType() in l1):
            return
        else:
            self.error()
        return

    def variableDeclaration(self):
        print("Variable Declaration")
        # id - 9
        if(self.lookAhead.getType() == TokenType.MP_IDENTIFIER):
            index = len(self.curTable.getTuples())
            self.identifierList()
            self.match(TokenType.MP_COLON)
            self.type()
            t = self.curTable.getTuples()
            for i in range(index, len(self.curTable.getTuples())):
                t[i].setType(self.idenType)

        else:
            self.error()
        return

    def type(self):
        print("Type")
        # boolean - 13
        if(self.lookAhead.getType() == TokenType.MP_BOOLEAN):
            self.match(TokenType.MP_BOOLEAN)
        # float - 11
        elif(self.lookAhead.getType() == TokenType.MP_FLOAT):
            self.match(TokenType.MP_FLOAT)
        # integer = 10
        elif(self.lookAhead.getType() == TokenType.MP_INTEGER):
            self.match(TokenType.MP_INTEGER)
        # string_lit - 12
        elif(self.lookAhead.getType() == TokenType.MP_STRING):
            self.match(TokenType.MP_STRING)
        else:
            self.error()
        return

    def procedureAndFunctionDeclarationPart(self):
        print("Procedure and Function Declaration Part")
        # begin -16
        if (self.lookAhead.getType() == TokenType.MP_BEGIN):
            return
        # function - 15
        elif (self.lookAhead.getType() == TokenType.MP_FUNCTION):
            self.functionDeclaration()
            self.procedureAndFunctionDeclarationPart()
            return
        # procedure - 14
        elif (self.lookAhead.getType() == TokenType.MP_PROCEDURE):
            self.procedureDeclaration()
            self.procedureAndFunctionDeclarationPart()
            return
        else:
            self.error()
        return

    def procedureDeclaration(self):
        print("Proceure Declaration")
        # procedure 17
        if (self.lookAhead.getType() == TokenType.MP_PROCEDURE):
            self.procedureHeading()
            self.match(TokenType.MP_SCOLON)
            self.block(False)
            self.match(TokenType.MP_SCOLON)
            return
        else:
            self.error()
        return

    def functionDeclaration(self):
        print("Function Declaration")
        # function 18
        if (self.lookAhead.getType() == TokenType.MP_FUNCTION):
            self.functionHeading()
            self.match(TokenType.MP_SCOLON)
            self.block(False)
            self.match(TokenType.MP_SCOLON)
            return
        else:
            self.error()
        return

    def procedureHeading(self):
        print("Procedure Heading")
        # procedure - 19
        if (self.lookAhead.getType() == TokenType.MP_PROCEDURE):
            self.match(TokenType.MP_PROCEDURE)
            self.procedureIdentifier()
            self.optionalFormalParameterList()
            return
        else:
            self.error()
        return

    def functionHeading(self):
        print("Function Heading")
        # function - 20
        if (self.lookAhead.getType() == TokenType.MP_FUNCTION):
            self.match(TokenType.MP_FUNCTION)
            self.functionIdentifier()
            self.optionalFormalParameterList()
            self.match(TokenType.MP_COLON)
            self.type()
            return
        else:
            self.error()
        return

    def optionalFormalParameterList(self):
        print("OPtional Formal Parameter List")
        # ; - 22
        if (self.lookAhead.getType() == TokenType.MP_SCOLON):
            return
        # : - 22
        elif (self.lookAhead.getType() == TokenType.MP_COLON):
            return
        # ( - 21
        elif (self.lookAhead.getType() == TokenType.MP_LPAREN):
            self.match(TokenType.MP_LPAREN)
            self.formalParameterSection()
            self.formalParameterSectionTail()
            self.match(TokenType.MP_RPAREN)
            return
        else:
            self.error()
        return

    def formalParameterSectionTail(self):
        print("Formal Parameter Section Tail")
        # ; - 23
        if (self.lookAhead.getType() == TokenType.MP_SCOLON):
            self.match(TokenType.MP_SCOLON)
            self.formalParameterSection()
            self.formalParameterSectionTail()
            return
        # ) - 24
        elif (self.lookAhead.getType() == TokenType.MP_RPAREN):
            return
        else:
            self.error()
        return

    def formalParameterSection(self):
        print("Formal Parameter Section")
        # var - 26
        if (self.lookAhead.getType() == TokenType.MP_VAR):
            self.variableParameterSection()
            return
        # id - 25
        elif (self.lookAhead.getType() == TokenType.MP_IDENTIFIER):
            self.valueParameterSection()
            return
        else:
            self.error()
        return

    def valueParameterSection(self):
        print("Value Parameter Section")
        # id - 27
        if (self.lookAhead.getType() == TokenType.MP_IDENTIFIER):
            self.identifierList()
            self.match(TokenType.MP_COLON)
            self.type()
            return
        else:
            self.error()
        return

    def variableParameterSection(self):
        print("Variable Parameter Section")
        # var - 28
        if (self.lookAhead.getType() == TokenType.MP_VAR):
            self.match(TokenType.MP_VAR)
            self.identifierList()
            self.match(TokenType.MP_COLON)
            self.type()
            return
        else:
            self.error()
        return

    def statementPart(self):
        print("Statement Part")
        # begin - 29
        if (self.lookAhead.getType() == TokenType.MP_BEGIN):
            self.compoundStatement()
            return
        else:
            self.error()
        return

    def compoundStatement(self):
        print("Compound Statement")
        # begin - 30
        if (self.lookAhead.getType() == TokenType.MP_BEGIN):
            self.match(TokenType.MP_BEGIN)
            self.statementSequence()
            self.match(TokenType.MP_END)
            return
        else:
            self.error()
        return

    def statementSequence(self):
        print("Statement Sequence")
        l1 = [TokenType.MP_BEGIN, TokenType.MP_END, TokenType.MP_FOR, TokenType.MP_IF, TokenType.MP_READ, TokenType.MP_REPEAT]
        l2 = [TokenType.MP_UNTIL, TokenType.MP_WHILE, TokenType.MP_WRITE, TokenType.MP_WRITELN, TokenType.MP_IDENTIFIER, TokenType.MP_SCOLON]
        # begin, end, for, if, read, repeat - 31
        if (self.lookAhead.getType() in l1):
            self.statement()
            self.statementTail()
            return
        # until, while, write, writeln, id, ; - 31
        elif (self.lookAhead.getType() in l2):
            self.statement()
            self.statementTail()
            return
        else:
            self.error()
        return

    def statementTail(self):
        print("Statement Tail")
        l1 = [TokenType.MP_END, TokenType.MP_UNTIL]
        # end, until - 33
        if (self.lookAhead.getType() in l1):
            return
        # ; - 32
        elif (self.lookAhead.getType() == TokenType.MP_SCOLON):
            self.match(TokenType.MP_SCOLON)
            self.statement()
            self.statementTail()
            return
        else:

            self.error()
        return

    def statement(self):
        print("Statement")
        l1 = [TokenType.MP_ELSE, TokenType.MP_END, TokenType.MP_UNTIL, TokenType.MP_SCOLON]
        l2 = [TokenType.MP_WRITE, TokenType.MP_WRITELN]
        # begin - 35
        if (self.lookAhead.getType() == TokenType.MP_BEGIN):
            self.compoundStatement()
            return
        # else, end, until, ; - 34
        elif (self.lookAhead.getType() in l1):
            self.emptyStatement()
            return
        # for - 42
        elif (self.lookAhead.getType() == TokenType.MP_FOR):
            self.forStatement()
            return
        # if - 39
        elif (self.lookAhead.getType() == TokenType.MP_IF):
            self.ifStatement()
            return
        # procedure 43
        elif (self.lookAhead.getType() == TokenType.MP_PROCEDURE):
            self.procedureStatement()
            return
        # read - 36
        elif (self.lookAhead.getType() == TokenType.MP_READ):
            self.readStatement()
            return
        # repeat - 41
        elif (self.lookAhead.getType() == TokenType.MP_REPEAT):
            self.repeatStatement()
            return
        # while - 40
        elif (self.lookAhead.getType() == TokenType.MP_WHILE):
            self.whileStatement()
            return
        # write, writeln - 37
        elif (self.lookAhead.getType() in l2):
            self.writeStatement()
            return
        elif (self.lookAhead.getType() == TokenType.MP_IDENTIFIER):
            # HERE
            if self.tokens[self.p + 1].getType() == TokenType.MP_ASSIGN:
                self.assignmentStatement()
            else:
                self.procedureStatement()

            return
        else:
            self.error()
        return

    def emptyStatement(self):
        print("Empty Statement")
        l1 = [TokenType.MP_ELSE, TokenType.MP_END, TokenType.MP_UNTIL, TokenType.MP_SCOLON]
        # else, end, until, ; - 44
        if (self.lookAhead.getType() in l1):
            return
        else:
            self.error()
        return

    def readStatement(self):
        print("Read Statement")
        # read - 45
        if (self.lookAhead.getType() == TokenType.MP_READ):
            self.match(TokenType.MP_READ)
            self.match(TokenType.MP_LPAREN)
            self.readParameter()
            self.readParameterTail()
            self.match(TokenType.MP_RPAREN)
            return
        else:
            self.error()
        return

    def readParameterTail(self):
        print("Read Parameter Tail")
        # ',' - 46
        if (self.lookAhead.getType() == TokenType.MP_COMMA):
            self.match(TokenType.MP_COMMA)
            self.readParameter()
            self.readParameterTail()
            return
        # ) - 47
        elif (self.lookAhead.getType() == TokenType.MP_RPAREN):
            return
        else:
            self.error()
        return

    def readParameter(self):
        print("Read Parameter")
        # id - 48
        if (self.lookAhead.getType() == TokenType.MP_IDENTIFIER):
            self.semanticAnalyzer.readStatement(self.tokens[self.p].getLexeme(), self.curTable)
            self.variableIdentifier()
            return
        else:
            self.error()
        return

    def writeStatement(self):
        print("Write Statement")
        # write - 49
        if (self.lookAhead.getType() == TokenType.MP_WRITE):
            self.match(TokenType.MP_WRITE)
            self.match(TokenType.MP_LPAREN)
            self.writeParameter(False)
            self.writeParameterTail(False)
            self.match(TokenType.MP_RPAREN)
            return
        # writeln - 50
        elif (self.lookAhead.getType() == TokenType.MP_WRITELN):
            self.match(TokenType.MP_WRITELN)
            self.match(TokenType.MP_LPAREN)
            self.writeParameter(True)
            self.writeParameterTail(True)
            self.match(TokenType.MP_RPAREN)
            return
        else:
            self.error()
        return

    def writeParameterTail(self, inLine):
        print("Write Parameter Tail")
        # ',' - 51
        if (self.lookAhead.getType() == TokenType.MP_COMMA):
            self.match(TokenType.MP_COMMA)

            # HERE
            self.writeParameter(inLine)
            self.writeParameterTail(inLine)
            return
        # ) - 52
        elif (self.lookAhead.getType() == TokenType.MP_RPAREN):
            return
        else:
            self.error()
        return

    def writeParameter(self, inLine):
        print("Write Parameter")
        l1 = [TokenType.MP_FALSE, TokenType.MP_NOT, TokenType.MP_TRUE, TokenType.MP_IDENTIFIER, TokenType.MP_INTEGER_LIT, TokenType.MP_FLOAT_LIT, TokenType.MP_STRING_LIT, TokenType.MP_LPAREN, TokenType.MP_PLUS, TokenType.MP_MINUS]
        # false, not, true, id, int_lit, float_lit, string_lit, (, +, '-' - 53
        if (self.lookAhead.getType() in l1):
            self.ordinalExpression()
            self.semanticAnalyzer.writeStatement(inLine)
            return
        else:
            self.error()
        return

    def assignmentStatement(self):
        print("Assignment Statement")
        # HERE HERE HERE HERE
        # id - 54, 55
        if (self.lookAhead.getType() == TokenType.MP_IDENTIFIER):
            thisToken = self.tokens[self.p]
            _type = self.curTable.getType(thisToken.getLexeme())
            self.curTable.printSymbolTable()
            print(thisToken.getLexeme())
            offset = self.curTable.getOffset(thisToken.getLexeme())

            self.variableIdentifier()
            self.match(TokenType.MP_ASSIGN)

            exprType = self.expression()

            self.semanticAnalyzer.assignment(_type, exprType, offset)

#            self.functionIdentifier()
#            self.match(TokenType.MP_ASSIGN)
#            self.expression()
            return
        else:
            self.error()
        return

    def ifStatement(self):
        print("If Statement")
        # if - 56
        if (self.lookAhead.getType() == TokenType.MP_IF):
            self.match(TokenType.MP_IF)
            boolExp = self.booleanExpression()
            if (boolExp == TokenType.MP_BOOLEAN):
                self.label += 2
                thisLabel = ("L%d" % (self.label - 1))
                elseLabel = ("L%d" % self.label)
                self.semanticAnalyzer.write("BRFS %s\n" % thisLabel)

                self.match(TokenType.MP_THEN)
                self.statement()
                self.semanticAnalyzer.write("BR %s\n" % elseLabel)
                self.semanticAnalyzer.write("%s:\n" % thisLabel)
                self.optionalElsePart()
                self.semanticAnalyzer.write("%s:\n" % elseLabel)
                return
        else:
            self.error()
        return

    def optionalElsePart(self):
        print("Optional Else Part")
        l1 = [TokenType.MP_END, TokenType.MP_UNTIL, TokenType.MP_SCOLON]
        # else - 57, 58
        if (self.lookAhead.getType() == TokenType.MP_ELSE):
            self.match(TokenType.MP_ELSE)
            self.statement()
            return
        # end, until, ; - 58
        elif (self.lookAhead.getType() in l1):
            return
        else:
            self.error()
        return

    def repeatStatement(self):
        print("Repeat Statement")
        # repeat - 59
        if (self.lookAhead.getType() == TokenType.MP_REPEAT):
            self.match(TokenType.MP_REPEAT)
            self.label += 1
            loopStart = ("L%s" % self.label)
            self.semanticAnalyzer.write("%s:\n" % loopStart)
            self.statementSequence()
            self.match(TokenType.MP_UNTIL)
            self.booleanExpression()
            self.semanticAnalyzer.write("BRFS %s\n" % loopStart)
            return
        else:
            self.error()
        return

    def whileStatement(self):
        print("While Statement")
        # while - 60
        if (self.lookAhead.getType() == TokenType.MP_WHILE):
            self.match(TokenType.MP_WHILE)
            self.label += 1
            conditionLabel = ("L%s" % self.label)
            self.label += 1
            endLabel = ("L%s" % self.label)
            self.semanticAnalyzer.write("%s:\n" % conditionLabel)
            self.booleanExpression()
            self.semanticAnalyzer.write("BRFS %s\n" % endLabel)
            self.match(TokenType.MP_DO)
            self.statement()
            self.semanticAnalyzer.write("BR %s\n" % conditionLabel)
            self.semanticAnalyzer.write("%s:\n" % endLabel)
            return
        else:
            self.error()
        return

    def forStatement(self):
        print("For Statement")
        # for - 61
        if (self.lookAhead.getType() == TokenType.MP_FOR):
            self.match(TokenType.MP_FOR)
            self.label += 2
            startLabel = ("L%d" % self.label)
            endLabel = ("L%d" % (self.label - 1))

            token = self.tokens[self.p]
            offset = self.curTable.getOffset(token.getLexeme())
            _type = self.curTable.getOffset(token.getType())

            self.controleVariable()
            self.match(TokenType.MP_ASSIGN)

            exprType = self.initialValue()
            self.semanticAnalyzer.assignment(_type, exprType, offset)
            step = self.stepValue()
            self.semanticAnalyzer.write("%s:\n" % startLabel)
            final = self.finalValue()
            self.semanticAnalyzer.write("PUSH %d(D0)\n" % offset)
            if step:
                self.semanticAnalyzer.expression(_type, final, "CMPLTS")
            else:
                self.semanticAnalyzer.expression(_type, final, "CMPGTS")

            self.match(TokenType.MP_DO)
            self.statement()

            if step:
                self.semanticAnalyzer.write("PUSH %d(D0)\n" % offset)
                self.semanticAnalyzer.write("PUSH #1\n")
                self.semanticAnalyzer.expression(_type, TokenType.MP_INTEGER, "ADDS")
                self.semanticAnalyzer.write("POP %d(D0)\n" % offset)
            else:
                self.semanticAnalyzer.write("PUSH %d(D0)\n" % offset)
                self.semanticAnalyzer.write("PUSH #1\n")
                self.semanticAnalyzer.expression(_type, TokenType.MP_INTEGER, "SUBS")
                self.semanticAnalyzer.write("POP %d(D0)\n" % offset)

            self.semanticAnalyzer.write("BR %s" % startLabel)
            self.semanticAnalyzer.write(endLabel)

            return
        else:
            self.error()
        return

    def controleVariable(self):
        print("Controle Variable")
        # id - 62
        if (self.lookAhead.getType() == TokenType.MP_IDENTIFIER):
            self.variableIdentifier()
            return
        else:
            self.error()
        return

    def initialValue(self):
        print("Initial Value")
        l1 = [TokenType.MP_FALSE, TokenType.MP_NOT, TokenType.MP_TRUE, TokenType.MP_IDENTIFIER, TokenType.MP_INTEGER_LIT, TokenType.MP_FLOAT_LIT, TokenType.MP_STRING_LIT, TokenType.MP_LPAREN, TokenType.MP_PLUS, TokenType.MP_MINUS]
        # false, not, true, id, int_lit, float_lit, string_lit, (, +, '-' - 63
        if (self.lookAhead.getType() in l1):
            self.ordinalExpression()
            return
        else:
            self.error()
        return

    def stepValue(self):
        print("Step Value")
        # downto - 65
        if (self.lookAhead.getType() == TokenType.MP_DOWNTO):
            self.match(TokenType.MP_DOWNTO)
            return False
        # to - 64
        elif (self.lookAhead.getType() == TokenType.MP_TO):
            self.match(TokenType.MP_TO)
            return True
        else:
            self.error()
        return

    def finalValue(self):
        print("Final Value")
        l1 = [TokenType.MP_FALSE, TokenType.MP_NOT, TokenType.MP_TRUE, TokenType.MP_IDENTIFIER, TokenType.MP_INTEGER_LIT, TokenType.MP_FLOAT_LIT, TokenType.MP_STRING_LIT, TokenType.MP_LPAREN, TokenType.MP_PLUS, TokenType.MP_MINUS]
        # false, not, true, id, int_lit, float_lit, string_lit, (, +, '-' - 66
        if(self.lookAhead.getType() in l1):
            self.ordinalExpression()
            return
        else:
            self.error()
        return

    def procedureStatement(self):
        print("Procedure Statement")
        # id - 67
        if (self.lookAhead.getType() == TokenType.MP_IDENTIFIER):
            self.procedureIdentifier()
            self.optionalActualParameterList()
            return
        else:
            self.error()
        return

    def optionalActualParameterList(self):
        print("Optional Actual Parameter List")
        l1 = [TokenType.MP_ELSE, TokenType.MP_END, TokenType.MP_UNTIL, TokenType.MP_SCOLON]
        # else, end, until, ; - 69
        if (self.lookAhead.getType() in l1):
            return
        # ( - 68
        elif (self.lookAhead.getType() == TokenType.MP_LPAREN):
            self.match(TokenType.MP_LPAREN)
            self.actualParameter()
            self.actualParameterTail()
            self.match(TokenType.MP_RPAREN)
            return
        else:
            self.error()
        return

    def actualParameterTail(self):
        print("Actual Parameter Tail")
        # ',' - 70
        if (self.lookAhead.getType() == TokenType.MP_COMMA):
            self.match(TokenType.MP_COMMA)
            self.actualParameter()
            self.actualParameterTail()
            return
        # ) - 71
        elif (self.lookAhead.getType() == TokenType.MP_RPAREN):
            return
        else:
            self.error()
        return

    def actualParameter(self):
        print("Actual Parameter")
        l1 = [TokenType.MP_FALSE, TokenType.MP_NOT, TokenType.MP_TRUE, TokenType.MP_IDENTIFIER, TokenType.MP_INTEGER_LIT, TokenType.MP_FLOAT_LIT, TokenType.MP_STRING_LIT, TokenType.MP_LPAREN, TokenType.MP_PLUS, TokenType.MP_MINUS]
        # false, not, true, id, int_lit, float_lit, string_lit, (, +, '-' - 72
        if (self.lookAhead.getType() in l1):
            self.ordinalExpression
            return
        else:
            self.error()
        return

    def expression(self):
        print("Expression")
        l1 = [TokenType.MP_FALSE, TokenType.MP_NOT, TokenType.MP_TRUE, TokenType.MP_IDENTIFIER, TokenType.MP_INTEGER_LIT, TokenType.MP_FLOAT_LIT, TokenType.MP_STRING_LIT, TokenType.MP_LPAREN, TokenType.MP_PLUS, TokenType.MP_MINUS]
        # false, not, true, id, int_lit, float_lit, string_lit, (, +, '-' - 73
        if (self.lookAhead.getType() in l1):
            term1Type = self.simpleExpression()
            boolCheck = self.optionalRelationalPart(term1Type)
            if (boolCheck):
                return TokenType.MP_BOOLEAN
            else:
                return term1Type
            return term1Type
        else:
            self.error()
        return

    def optionalRelationalPart(self, term1Type):
        print("Optional Relational Part")
        l1 = [TokenType.MP_DO, TokenType.MP_DOWNTO, TokenType.MP_ELSE, TokenType.MP_END, TokenType.MP_THEN, TokenType.MP_TO, TokenType.MP_UNTIL, TokenType.MP_COMMA, TokenType.MP_SCOLON, TokenType.MP_LPAREN, TokenType.MP_RPAREN]
        l2 = [TokenType.MP_EQUAL, TokenType.MP_GTHAN, TokenType.MP_LTHAN, TokenType.MP_LEQUAL, TokenType.MP_GEQUAL, TokenType.MP_NEQUAL]
        # do, downto, else, end, then, to, until, ',', ;, ( - 75
        if (self.lookAhead.getType() in l1):
            return False
        # =, >, <, <=, >=, <> - 74
        elif (self.lookAhead.getType() in l2):
            operator = self.relationalOperator()
            term2Type = self.simpleExpression()
            self.semanticAnalyzer.expression(term1Type, term2Type, operator)
            return True
        else:
            self.error()
        return

    def relationalOperator(self):
        print("Relational Operator")
        # = - 76
        if (self.lookAhead.getType() == TokenType.MP_EQUAL):
            self.match(TokenType.MP_EQUAL)
            return "CMPEQS"
            return
        # > - 78
        elif (self.lookAhead.getType() == TokenType.MP_GTHAN):
            self.match(TokenType.MP_GTHAN)
            return "CMPGTS"
        # < - 77
        elif (self.lookAhead.getType() == TokenType.MP_LTHAN):
            self.match(TokenType.MP_LTHAN)
            return "CMPLTS"
        # <= - 79
        elif (self.lookAhead.getType() == TokenType.MP_LEQUAL):
            self.match(TokenType.MP_LEQUAL)
            return "CMPLES"
        # >= - 80
        elif (self.lookAhead.getType() == TokenType.MP_GEQUAL):
            self.match(TokenType.MP_GEQUAL)
            return "CMPGES"
        # <> - 81
        elif (self.lookAhead.getType() == TokenType.MP_NEQUAL):
            self.match(TokenType.MP_NEQUAL)
            return"CMPNES"
        else:
            self.error()
        return

    def simpleExpression(self):
        print("Simple Expression")
        l1 = [TokenType.MP_FALSE, TokenType.MP_NOT, TokenType.MP_TRUE, TokenType.MP_IDENTIFIER, TokenType.MP_INTEGER_LIT, TokenType.MP_FLOAT_LIT, TokenType.MP_STRING_LIT, TokenType.MP_LPAREN, TokenType.MP_PLUS, TokenType.MP_MINUS]
        # false, not, true, id, int_lit, float_lit, string_lit, (, +, '-' - 82
        if (self.lookAhead.getType() in l1):
            sign = self.optionalSign()
            term1 = self.term()

            if (sign):
                self.semanticAnalyzer.pushLitToStack("-1")
                self.semanticAnalyzer.expression(term1, "MP_INTEGER", "MULS")

            self.termTail(term1)
            return term1
        else:
            self.error()
        return

    def termTail(self, term1):
        print("Term Tail")
        l1 = [TokenType.MP_DO, TokenType.MP_DOWNTO, TokenType.MP_ELSE, TokenType.MP_END, TokenType.MP_THEN, TokenType.MP_TO, TokenType.MP_UNTIL]
        l2 = [TokenType.MP_COMMA, TokenType.MP_SCOLON, TokenType.MP_RPAREN, TokenType.MP_EQUAL, TokenType.MP_GTHAN, TokenType.MP_LTHAN, TokenType.MP_GEQUAL, TokenType.MP_LEQUAL, TokenType.MP_NEQUAL]
        l3 = [TokenType.MP_OR, TokenType.MP_PLUS, TokenType.MP_MINUS]
        # do, downto, else, end, then, to, until - 84
        if (self.lookAhead.getType() in l1):
            return
        # ',', ;, ), =, >, <, <=, >=, <> - 84
        elif (self.lookAhead.getType() in l2):
            return
        # or, +, '-' - 83
        elif (self.lookAhead.getType() in l3):
            operator = self.addingOperator()
            term2 = self.term()
            self.semanticAnalyzer.expression(term1, term2, operator)
            self.termTail(term1)
            return
        else:
            self.error()
        return

    def optionalSign(self):
        print("Optional Sign")
        l1 = [TokenType.MP_FALSE, TokenType.MP_NOT, TokenType.MP_TRUE, TokenType.MP_IDENTIFIER, TokenType.MP_INTEGER_LIT, TokenType.MP_FLOAT_LIT, TokenType.MP_STRING_LIT, TokenType.MP_LPAREN]
        # false, not, true, id, int_lit, float_lit, string_lit, ( - 87
        if (self.lookAhead.getType() in l1):
            return
        # +, - 85
        elif (self.lookAhead.getType() == TokenType.MP_PLUS):
            self.match(TokenType.MP_PLUS)
            return
        # '-' - 86
        elif (self.lookAhead.getType() == TokenType.MP_MINUS):
            self.match(TokenType.MP_MINUS)
            return True
        else:
            self.error()
        return False

    def addingOperator(self):
        print("Adding Operator")
        # or - 90
        if (self.lookAhead.getType() == TokenType.MP_OR):
            self.match(TokenType.MP_OR)
            return "ORS"
        # + - 88
        elif (self.lookAhead.getType() == TokenType.MP_PLUS):
            self.match(TokenType.MP_PLUS)
            return "ADDS"
        # '-' - 89
        elif (self.lookAhead.getType() == TokenType.MP_MINUS):
            self.match(TokenType.MP_MINUS)
            return "SUBS"
        else:
            self.error()
        return

    def term(self):
        print("Term")
        l1 = [TokenType.MP_FALSE, TokenType.MP_NOT, TokenType.MP_TRUE, TokenType.MP_IDENTIFIER, TokenType.MP_INTEGER_LIT, TokenType.MP_FLOAT_LIT, TokenType.MP_STRING_LIT, TokenType.MP_LPAREN]
        # false, not, true, id, int_lit, float_lit, string_lit, ( - 91
        if (self.lookAhead.getType() in l1):
            term1 = self.factor()
            self.factorTail(term1)
            return term1
        else:
            self.error()
        return

    def factorTail(self, term1Type):
        print("Factor Tail")
        l1 = [TokenType.MP_AND, TokenType.MP_DIV, TokenType.MP_MOD, TokenType.MP_TIMES, TokenType.MP_FLOAT_DIVIDE]
        l2 = [TokenType.MP_DO, TokenType.MP_DOWNTO, TokenType.MP_ELSE, TokenType.MP_END, TokenType.MP_OR, TokenType.MP_THEN, TokenType.MP_TO, TokenType.MP_UNTIL]
        l3 = [TokenType.MP_COMMA, TokenType.MP_SCOLON, TokenType.MP_RPAREN, TokenType.MP_EQUAL, TokenType.MP_GTHAN, TokenType.MP_LTHAN, TokenType.MP_GEQUAL, TokenType.MP_LEQUAL, TokenType.MP_NEQUAL, TokenType.MP_PLUS, TokenType.MP_MINUS]
        # and, div, mod, *, / - 92
        if (self.lookAhead.getType() in l1):
            operator = self.multiplyingOperator()
            term2Type = self.factor()
            self.semanticAnalyzer.expression(term1Type, term2Type, operator)
            self.factorTail(term1Type)
            return
        # do, downto, else, end, or, then, to, until - 93
        elif (self.lookAhead.getType() in l2):
            return
        # ',', ;, ), =, >, <, <=, >=, <>, +, '-' - 93
        elif (self.lookAhead.getType() in l3):
            return
        else:
            self.error()
        return

    def multiplyingOperator(self):
        print("Multiplying Operator")
        # and - 98
        if (self.lookAhead.getType() == TokenType.MP_AND):
            self.match(TokenType.MP_AND)
            return "ANDS"
        # div - 96
        elif (self.lookAhead.getType() == TokenType.MP_DIV):
            self.match(TokenType.MP_DIV)
            return "DIVS"
        # mod - 97
        elif (self.lookAhead.getType() == TokenType.MP_MOD):
            self.match(TokenType.MP_MOD)
            return "MODS"
        # * - 94
        elif (self.lookAhead.getType() == TokenType.MP_TIMES):
            self.match(TokenType.MP_TIMES)
            return "MULS"
        # / - 95
        elif (self.lookAhead.getType() == TokenType.MP_FLOAT_DIVIDE):
            self.match(TokenType.MP_FLOAT_DIVIDE)
            return "DIVSF"
        else:
            self.error()
        return

    def factor(self):
        print("Factor")
        # false - 103
        if (self.lookAhead.getType() == TokenType.MP_FALSE):
            self.match(TokenType.MP_FALSE)
            self.semanticAnalyzer.pushLitToStack("0")
            return TokenType.MP_BOOLEAN
        # not - 104
        elif (self.lookAhead.getType() == TokenType.MP_NOT):
            self.match(TokenType.MP_NOT)
            self.factor()
            self.semanticAnalyzer.write("NOTS\n")
            return TokenType.MP_BOOLEAN
        # true - 102
        elif (self.lookAhead.getType() == TokenType.MP_TRUE):
            self.match(TokenType.MP_TRUE)
            self.semanticAnalyzer.pushLitToStack("1")
            return TokenType.MP_BOOLEAN
        # HERE HERE HERE HERE
        # id - 106, 116
        elif (self.lookAhead.getType() == TokenType.MP_IDENTIFIER):
            #self.functionIdentifier()
            #self.optionalActualParameterList()
            self.semanticAnalyzer.pushToStack(self.tokens[self.p].getLexeme(), self.curTable)

            self.variableIdentifier()
            return
        # int_lit - 99
        elif (self.lookAhead.getType() == TokenType.MP_INTEGER_LIT):
            self.semanticAnalyzer.pushLitToStack(self.tokens[self.p].getLexeme())
            self.match(TokenType.MP_INTEGER_LIT)
            return TokenType.MP_INTEGER
        # float_lit - 100
        elif (self.lookAhead.getType() == TokenType.MP_FLOAT_LIT):
            self.semanticAnalyzer.pushLitToStack(self.tokens[self.p].getLexeme())
            self.match(Token.MP_FLOAT_LIT)
            return TokenType.MP_FLOAT
        # string_lit - 101
        elif (self.lookAhead.getType() == TokenType.MP_STRING_LIT):
            self.semanticAnalyzer.pushLitToStack(self.tokens[self.p].getLexeme())
            self.match(TokenType.MP_STRING_LIT)
            return TokenType.MP_STRING
        # ( - 105
        elif (self.lookAhead.getType() == TokenType.MP_LPAREN):
            self.match(TokenType.MP_LPAREN)
            val = self.expression()
            self.match(TokenType.MP_RPAREN)
            return val
        else:
            self.error()
        return

    def programIdentifier(self):
        print("Program Identifier")
        # id - 107
        if (self.lookAhead.getType() == TokenType.MP_IDENTIFIER):
            self.match(TokenType.MP_IDENTIFIER)
            return
        else:
            self.error()
        return

    def variableIdentifier(self):
        print("Variable Identifier")
        # id - 108
        if (self.lookAhead.getType() == TokenType.MP_IDENTIFIER):
            self.match(TokenType.MP_IDENTIFIER)
            return
        else:
            self.error()
        return

    def procedureIdentifier(self):
        print("Procedure Identifier")
        # id - 109
        if (self.lookAhead.getType() == TokenType.MP_IDENTIFIER):
            self.match(TokenType.MP_IDENTIFIER)
            return
        else:
            self.error()
        return

    def functionIdentifier(self):
        print("Function Identifier")
        # id - 110
        if (self.lookAhead.getType() == TokenType.MP_IDENTIFIER):
            self.match(TokenType.MP_IDENTIFIER)
            return
        else:
            self.error()
        return

    def booleanExpression(self):
        print("Boolean Expression")
        l1 = [TokenType.MP_FALSE, TokenType.MP_NOT, TokenType.MP_TRUE, TokenType.MP_IDENTIFIER, TokenType.MP_INTEGER_LIT, TokenType.MP_FLOAT_LIT, TokenType.MP_STRING_LIT, TokenType.MP_LPAREN, TokenType.MP_PLUS, TokenType.MP_MINUS]
        # false, not, true, id, int_lit, float_lit, string_lit, (, +, '-' - 111
        if (self.lookAhead.getType() in l1):
            res = self.expression()
            return res
        else:
            self.error()
        return

    def ordinalExpression(self):
        print("Ordinal Expression")
        l1 = [TokenType.MP_FALSE, TokenType.MP_NOT, TokenType.MP_TRUE, TokenType.MP_IDENTIFIER, TokenType.MP_INTEGER_LIT, TokenType.MP_FLOAT_LIT, TokenType.MP_STRING_LIT, TokenType.MP_LPAREN, TokenType.MP_PLUS, TokenType.MP_MINUS]
        # false, not, true, id, int_lit, float_lit, string_lit, (, +, '-' - 112
        if (self.lookAhead.getType() in l1):
            self.expression()
            return
        else:
            self.error()
        return

    def identifierList(self):
        print("Identifier List")
        # id - 113
        if (self.lookAhead.getType() == TokenType.MP_IDENTIFIER):
            token = self.tokens[self.p]
            aSymbol = Symbol.Symbol(token.getLexeme(), self.idenType, self.idenKind, self.curTable.getNumTuples(), None)
            self.curTable.insert(aSymbol)

            self.match(TokenType.MP_IDENTIFIER)
            self.identifierTail()
            return
        else:
            self.error()
        return

    def identifierTail(self):
        print("Identifier Tail")
        # ',' - 114
        if (self.lookAhead.getType() == TokenType.MP_COMMA):
            self.match(TokenType.MP_COMMA)
            token = self.tokens[self.p]
            aSymbol = Symbol.Symbol(token.getLexeme(), self.idenType, self.idenKind, self.curTable.getNumTuples(), None)
            self.curTable.insert(aSymbol)

            self.match(TokenType.MP_IDENTIFIER)
            self.identifierTail()
            return
        # : - 115
        elif (self.lookAhead.getType() == TokenType.MP_COLON):
            return
        else:
            self.error()
        return

    def match(self, tokenType):
        print("Matched: %s" % (tokenType))
        if self.lookAhead.getType() == tokenType:
            self.idenType = self.lookAhead.getType()
            self.p = self.p + 1
            if self.p < len(self.tokens):
                self.lookAhead = self.tokens[self.p]
        else:
            self.error()

    def error(self):
        t = self.lookAhead
        print("Error at line %s, column %s: found %s" % (t.getLineNumber(), t.getColumnNumber(), t.getType()))
