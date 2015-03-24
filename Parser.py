# PARSER
import sys
import Lexeme, Token, Scanner
from TokenType import TokenType

class Parser:
	tokens = []
	lookAhead = None
	p = 0

	def __init__(self):
		self.tokens = []
		self.lookAhead = None
		self.p = 0

	def addToken(self, inToken):
		self.tokens.append(inToken)

	def printTokens(self):
		for t in self.tokens:
			t.printToken()

	def checkGrammar(self):
		self.lookAhead = self.tokens[self.p]
		self.systemGoal()
		return

	def systemGoal(self):
		# program - 1
		if (self.lookAhead.getType() == TokenType.MP_PROGRAM):
			self.program()
			self.match(TokenType.MP_EOF)
		else:
			self.error()
		return

	def program(self):
		# program - 2
		if (self.lookAhead.getType() == TokenType.MP_PROGRAM):
			self.programHeading()
			self.match(TokenType.MP_SCOLON)
			self.block()
		else:
			self.error()
		return

	def programHeading(self):
		# program - 3
		if (self.lookAhead.getType() == TokenType.MP_PROGRAM):
			self.match(TokenType.MP_PROGRAM)
			self.programIdentifier()
		else:
			self.error()
		return

	def block(self):
		l1 = [TokenType.MP_BEGIN, TokenType.MP_FUNCTION, TokenType.MP_PROCEDURE, TokenType.MP_VAR]
		# begin, function, procedure, var - 4
		if (self.lookAhead.getType() in l1):
			self.variableDeclarationPart()
			self.procedureAndFunctionDeclarationPart()
			self.statementPart()
		else:
			self.error()
		return

	def variableDeclarationPart(self):
		l1 = [TokenType.MP_BEGIN, TokenType.MP_FUNCTION, TokenType.MP_PROCEDURE]
		# var - 5
		if (self.lookAhead.getType() == TokenType.MP_VAR):
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
		# id - 9
		if(self.lookAhead.getType() == TokenType.MP_IDENTIFIER):
			self.identifierList()
			self.match(TokenType.MP_COLON)
			self.type()
		else:
			self.error()
		return

	# HERE
	def type(self):
		l = [TokenType.MP_TRUE, TokenType.MP_FALSE, TokenType.MP_FLOAT, TokenType.MP_INTEGER]
		# HERE HERE HERE HERE mp_boolean vs. mp_true & mp_false?
		# boolean - 13
		if(self.lookAhead.getType() == TokenType.MP_TRUE):
			self.match(TokenType.MP_TRUE)
		# boolean - 13
		elif(self.lookAhead.getType() == TokenType.MP_FALSE):
			self.match(TokenType.MP_FALSE)
		# float - 11
		elif(self.lookAhead.getType() == TokenType.MP_FLOAT):
			self.match(TokenType.MP_FLOAT)
		# integer = 10
		elif(self.lookAhead.getType() == TokenType.MP_INTEGER):
			self.match(TokenType.MP_INTEGER)
		# HERE HERE HERE HERE do i match string_lit or just string?
		# string_lit - 12
		elif(self.lookAhead.getType() == TokenType.MP_STRING_LIT):
			self.match(TokenType.MP_STRING_LIT)
		else:
			self.error(l)
		return

	def procedureAndFunctionDeclarationPart(self):
		# begin -16 
		if (self.lookAhead.getType() == TokenType.MP_BEGIN):
			return
		# function - 15
		elif (self.lookAhead.getType() == TokenType.MP_FUNCTION):
			return
		# procedure - 14
		elif (self.lookAhead.getType() == TokenType.MP_PROCEDURE):
			return
		else:
			self.error()
		return

	def procedureDeclaration(self):
		# procedure 17
		if (self.lookAhead.getType() == TokenType.MP_PROCEDURE):
			return
		else:
			self.error()
		return

	def functionDeclaration(self):
		# function 18
		if (self.lookAhead.getType() == TokenType.MP_FUNCTION):
			return
		else:
			self.error()
		return

	def procedureHeading(self):
		# procedure - 19
		if (self.lookAhead.getType() == TokenType.MP_PROCEDURE):
			return
		else:
			self.error()
		return

	def functionHeading(self):
		# function - 20
		if (self.lookAhead.getType() == TokenType.MP_FUNCTION):
			return
		else:
			self.error()
		return

	def optionalFormalParameterList(self):
		# ; - 22
		if (self.lookAhead.getType() == TokenType.MP_SCOLON):
			return
		# : - 22
		elif (self.lookAhead.getType() == TokenType.MP_COLON):
			return
		# ( - 21
		elif (self.lookAhead.getType() == TokenType.MP_LPAREN):
			return
		else:
			self.error()
		return

	def formalParameterSectionTail(self):
		# ; - 23
		if (self.lookAhead.getType() == TokenType.MP_SCOLON):
			return
		# ) - 24
		elif (self.lookAhead.getType() == TokenType.MP_RPAREN):
			return
		else:
			self.error()
		return

	def formalParameterSection(self):
		# var - 26
		if (self.lookAhead.getType() == TokenType.MP_VAR):
			return
		# id - 25
		elif (self.lookAhead.getType() == TokenType.MP_IDENTIFIER):
			return
		else:
			self.error()
		return

	def valueParameterSection(self):
		# id - 27
		if (self.lookAhead.getType() == TokenType.MP_IDENTIFIER):
			return
		else:
			self.error()
		return

	def variableParameterSection(self):
		# var - 28
		if (self.lookAhead.getType() == TokenType.MP_VAR):
			return
		else:
			self.error()
		return

	def statementPart(self):
		# begin - 29
		if (self.lookAhead.getType() == TokenType.MP_BEGIN):
			return
		else:
			self.error()
		return

	def compoundStatement(self):
		# begin - 30
		if (self.lookAhead.getType() == TokenType.MP_BEGIN):
			return
		else:
			self.error()
		return

	def statementSequence(self):
		l1 = [TokenType.MP_BEGIN, TokenType.MP_END, TokenType.MP_FOR, TokenType.MP_IF, TokenType.MP_READ, TokenType.MP_REPEAT]
		l2 = [TokenType.MP_UNTIL, TokenType.MP_WHILE, TokenType.MP_WRITE, TokenType.MP_WRITELN, TokenType.MP_IDENTIFIER, TokenType.MP_SCOLON]
		# begin, end, for, if, read, repeat - 31
		if (self.lookAhead.getType() in l1):
			return
		# until, while, write, writeln, id, ; - 31
		elif (self.lookAhead.getType() in l2 ):
			return
		else:
			self.error()
		return

	def statementTail(self):
		l1 = [TokenType.MP_ELSE, TokenType.MP_UNTIL]
		# else, until - 33
		if (self.lookAhead.getType() in l1 ):
			return
		# ; - 32
		elif (self.lookAhead.getType() == TokenType.MP_SCOLON):
			return
		else:
			self.error()
		return

	def statement(self):
		l1 = [TokenType.MP_ELSE, TokenType.MP_END, TokenType.MP_UNTIL, TokenType.MP_SCOLON]
		l2 = [TokenType.MP_WRITE, TokenType.MP_WRITELN]
		# begin - 35
		if (self.lookAhead.getType() == TokenType.MP_BEGIN):
			return
		# else, end, until, ; - 34
		elif (self.lookAhead.getType() in l1 ):
			return
		# for - 42
		elif (self.lookAhead.getType() == TokenType.MP_FOR):
			return
		# if - 39
		elif (self.lookAhead.getType() == TokenType.MP_IF):
			return
		# procedure 43
		elif (self.lookAhead.getType() == TokenType.MP_PROCEDURE):
			return
		# read - 36
		elif (self.lookAhead.getType() == TokenType.MP_READ):
			return
		# repeat - 41
		elif (self.lookAhead.getType() == TokenType.MP_REPEAT):
			return
		# while - 40
		elif (self.lookAhead.getType() == TokenType.MP_WHILE):
			return
		# write, writeln - 37
		elif (self.lookAhead.getType() in l2 ):
			return
		# HERE HERE HERE HERE
		# id - 38,43
		elif (self.lookAhead.getType() == TokenType.MP_IDENTIFIER):
			return
		else:
			self.error()
		return

	def emptyStatement(self):
		l1 = [TokenType.MP_ELSE, TokenType.MP_END, TokenType.MP_UNTIL, TokenType.MP_SCOLON]
		# else, end, until, ; - 44
		if (self.lookAhead.getType() in l1):
			return
		else:
			self.error()
		return

	def readStatement(self):
		# read - 45
		if (self.lookAhead.getType() == TokenType.MP_READ):
			return
		else:
			self.error()
		return

	def readParameterTail(self):
		# ',' - 46
		if (self.lookAhead.getType() == TokenType.MP_COMMA):
			return
		# ) - 47
		elif (self.lookAhead.getType() == TokenType.MP_RPAREN):
			return
		else:
			self.error()
		return

	def readParameter(self):
		# id - 48
		if (self.lookAhead.getType() == TokenType.MP_IDENTIFIER):
			return
		else:
			self.error()
		return

	def writeStatement(self):
		# write - 49
		if (self.lookAhead.getType() == TokenType.MP_WRITE):
			return
		# writeln - 50
		elif (self.lookAhead.getType() == TokenType.MP_WRITELN):
			return
		else:
			self.error()
		return

	def writeParameterTail(self):
		# ',' - 51
		if (self.lookAhead.getType() == TokenType.MP_COMMA):
			return
		# ) - 52
		elif (self.lookAhead.getType() == TokenType.MP_RPAREN):
			return
		else:
			self.error()
		return

	def writeParameter(self):
		l1 = [TokenType.MP_FALSE, TokenType.MP_NOT, TokenType.MP_TRUE, TokenType.MP_IDENTIFIER, TokenType.MP_INTEGER_LIT, TokenType.MP_FLOAT_LIT, TokenType.MP_STRING_LIT, TokenType.MP_LPAREN, TokenType.MP_PLUS, TokenType.MP_MINUS]
		# false, not, true, id, int_lit, float_lit, string_lit, (, +, '-' - 53
		if (self.lookAhead.getType() in l1):
			return
		else:
			self.error()
		return

	def assignmentStatement(self):
		# id - 54, 55
		if (self.lookAhead.getType() == TokenType.MP_IDENTIFIER):
			return
		else:
			self.error()
		return

	def ifStatement(self):
		# if - 56
		if (self.lookAhead.getType() == TokenType.MP_IF):
			return
		else:
			self.error()
		return

	def optionalElsePart(self):
		l1 = [TokenType.MP_END, TokenType.MP_UNTIL, TokenType.MP_SCOLON]
		# HERE HERE HERE HERE
		# else - 57, 58
		if (self.lookAhead.getType() == TokenType):
			return
		# end, until, ; - 58
		elif (self.lookAhead.getType() in l1 ):
			return
		else:
			self.error()
		return

	def repeatStatement(self):
		# repeat - 59
		if (self.lookAhead.getType() == TokenType.MP_REPEAT):
			return
		else:
			self.error()
		return

	def whileStatement(self):
		# while - 60
		if (self.lookAhead.getType() == TokenType.MP_WHILE):
			return
		else:
			self.error()
		return

	def forStatement(self):
		# for - 61
		if (self.lookAhead.getType() == TokenType.MP_FOR):
			return
		else:
			self.error()
		return

	def controleVariable(self):
		# id - 62
		if (self.lookAhead.getType() == TokenType.MP_IDENTIFIER):
			return
		else:
			self.error()
		return

	def initialValue(self):
		l1 = [TokenType.MP_FALSE, TokenType.MP_NOT, TokenType.MP_TRUE, TokenType.MP_IDENTIFIER, TokenType.MP_INTEGER_LIT, TokenType.MP_FLOAT_LIT, TokenType.MP_STRING_LIT, TokenType.MP_LPAREN, TokenType.MP_PLUS, TokenType.MP_MINUS]
		# false, not, true, id, int_lit, float_lit, string_lit, (, +, '-' - 63
		if (self.lookAhead.getType() in l1):
			return
		else:
			self.error()
		return

	def stepValue(self):
		# downto - 65
		if (self.lookAhead.getType() == TokenType.MP_DOWNTO):
			return
		# to - 64
		elif (self.lookAhead.getType() == TokenType.MP_TO):
			return
		else:
			self.error()
		return

	def finalValue(self):
		l1 = [TokenType.MP_FALSE, TokenType.MP_NOT, TokenType.MP_TRUE, TokenType.MP_IDENTIFIER, TokenType.MP_INTEGER_LIT, TokenType.MP_FLOAT_LIT, TokenType.MP_STRING_LIT, TokenType.MP_LPAREN, TokenType.MP_PLUS, TokenType.MP_MINUS]
		# false, not, true, id, int_lit, float_lit, string_lit, (, +, '-' - 66
		if(self.lookAhead.getType() in l1):
			return
		else:
			self.error()
		return

	def procedureStatement(self):
		# id - 67
		if (self.lookAhead.getType() == TokenType.MP_IDENTIFIER):
			return
		else:
			self.error()
		return

	def optionalActualParameterList(self):
		l1 = [TokenType.MP_ELSE, TokenType.MP_END, TokenType.MP_UNTIL, TokenType.MP_SCOLON]
		# else, end, until, ; - 69
		if (self.lookAhead.getType() in l1):
			return
		# ( - 68
		elif (self.lookAhead.getType() == TokenType.MP_LPAREN):
			return
		else:
			self.error()
		return

	def actualParameterTail(self):
		# ',' - 70
		if (self.lookAhead.getType() == TokenType.MP_COMMA):
			return
		# ) - 71
		elif (self.lookAhead.getType() == TokenType.MP_RPAREN):
			return
		else:
			self.error()
		return

	def actualParameter(self):
		l1 = [TokenType.MP_FALSE, TokenType.MP_NOT, TokenType.MP_TRUE, TokenType.MP_IDENTIFIER, TokenType.MP_INTEGER_LIT, TokenType.MP_FLOAT_LIT, TokenType.MP_STRING_LIT, TokenType.MP_LPAREN, TokenType.MP_PLUS, TokenType.MP_MINUS]
		# false, not, true, id, int_lit, float_lit, string_lit, (, +, '-' - 72
		if (self.lookAhead.getType() in l1):
			return
		else:
			self.error()
		return

	def expression(self):
		l1 = [TokenType.MP_FALSE, TokenType.MP_NOT, TokenType.MP_TRUE, TokenType.MP_IDENTIFIER, TokenType.MP_INTEGER_LIT, TokenType.MP_FLOAT_LIT, TokenType.MP_STRING_LIT, TokenType.MP_LPAREN, TokenType.MP_PLUS, TokenType.MP_MINUS]
		# false, not, true, id, int_lit, float_lit, string_lit, (, +, '-' - 73
		if (self.lookAhead.getType() in l1):
			return
		else:
			self.error()
		return

	def optionalRelationalPart(self):
		l1 = [TokenType.MP_DO, TokenType.MP_DOWNTO, TokenType.MP_ELSE, TokenType.MP_END, TokenType.MP_THEN, TokenType.MP_TO, TokenType.MP_UNTIL, TokenType.MP_COMMA, TokenType.MP_SCOLON, TokenType.MP_LPAREN]
		l2 = [TokenType.MP_EQUAL, TokenType.MP_GTHAN, TokenType.MP_LTHAN, TokenType.MP_LEQUAL, TokenType.MP_GEQUAL, TokenType.MP_NEQUAL]
		# do, downto, else, end, then, to, until, ',', ;, ( - 75
		if (self.lookAhead.getType() in l1):
			return
		# =, >, <, <=, >=, <> - 74
		elif (self.lookAhead.getType() in l2):
			return
		else:
			self.error()
		return

	def relationalOperator(self):
		# = - 76
		if (self.lookAhead.getType() == TokenType.MP_EQUAL):
			return
		# > - 78
		elif (self.lookAhead.getType() == TokenType.MP_GTHAN):
			return
		# < - 77
		elif (self.lookAhead.getType() == TokenType.MP_LTHAN):
			return
		# <= - 79
		elif (self.lookAhead.getType() == TokenType.MP_LEQUAL):
			return
		# >= - 80
		elif (self.lookAhead.getType() == TokenType.MP_GEQUAL):
			return
		# <> - 81
		elif (self.lookAhead.getType() == TokenType.MP_NEQUAL):
			return
		else:
			self.error()
		return

	def simpleExpression(self):
		l1 = [TokenType.MP_FALSE, TokenType.MP_NOT, TokenType.MP_TRUE, TokenType.MP_IDENTIFIER, TokenType.MP_INTEGER_LIT, TokenType.MP_FLOAT_LIT, TokenType.MP_STRING_LIT, TokenType.MP_LPAREN, TokenType.MP_PLUS, TokenType.MP_MINUS]
		# false, not, true, id, int_lit, float_lit, string_lit, (, +, '-' - 82
		if (self.lookAhead.getType() in l1):
			return
		else:
			self.error()
		return

	def termTail(self):
		l1 = [TokenType.MP_DO, TokenType.MP_DOWNTO, TokenType.MP_ELSE, TokenType.MP_END, TokenType.MP_THEN, TokenType.MP_TO, TokenType.MP_UNTIL]
		l2 = [TokenType.MP_COMMA, TokenType.MP_SCOLON, TokenType.MP_RPAREN, TokenType.MP_EQUAL, TokenType.MP_GTHAN, TokenType.MP_LTHAN, TokenType.MP_GEQUAL, TokenType.MP_LEQUAL, TokenType.MP_NEQUAL]
		l3 = [TokenType.MP_OR, TokenType.MP_PLUS, TokenType.MP_MINUS]
		# do, downto, else, end, then, to, until - 84
		if (self.lookAhead.getType() in l1 ):
			return
		# ',', ;, ), =, >, <, <=, >=, <> - 84
		elif (self.lookAhead.getType() in l2):
			return
		# or, +, '-' - 83
		elif (self.lookAhead.getType() in l3 ):
			return
		else:
			self.error()
		return

	def optionalSign(self):
		l1 = [TokenType.MP_FALSE, TokenType.MP_NOT, TokenType.MP_TRUE, TokenType.MP_IDENTIFIER, TokenType.MP_INTEGER_LIT, TokenType.MP_FLOAT_LIT, TokenType.MP_STRING_LIT, TokenType.MP_LPAREN]
		# false, not, true, id, int_lit, float_lit, string_lit, ( - 87
		if (self.lookAhead.getType() in l1):
			return
		# +, - 85
		elif (self.lookAhead.getType() == TokenType.MP_PLUS):
			return
		# '-' - 86
		elif (self.lookAhead.getType() == TokenType.MP_MINUS):
			return
		else:
			self.error()
		return

	def addingOperator(self):
		# or - 90
		if (self.lookAhead.getType() == TokenType.MP_OR):
			return
		# + - 88
		elif (self.lookAhead.getType() == TokenType.MP_PLUS):
			return
		# '-' - 89
		elif (self.lookAhead.getType() == TokenType.MP_MINUS):
			return
		else:
			self.error()
		return

	def term(self):
		l1 = [TokenType.MP_FALSE, TokenType.MP_NOT, TokenType.MP_TRUE, TokenType.MP_IDENTIFIER, TokenType.MP_INTEGER_LIT, TokenType.MP_FLOAT_LIT, TokenType.MP_STRING_LIT, TokenType.MP_LPAREN]
		# false, not, true, id, int_lit, float_lit, string_lit, ( - 91
		if (self.lookAhead.getType() in l1):
			return
		else:
			self.error()
		return

	def factorTail(self):
		l1 = [TokenType.MP_AND, TokenType.MP_DIV, TokenType.MP_MOD, TokenType.MP_TIMES, TokenType.MP_FLOAT_DIVIDE]
		l2 = [TokenType.MP_DO, TokenType.MP_DOWNTO, TokenType.MP_ELSE, TokenType.MP_END, TokenType.MP_OR, TokenType.MP_THEN, TokenType.MP_TO, TokenType.MP_UNTIL]
		l3 = [TokenType.MP_COMMA, TokenType.MP_SCOLON, TokenType.MP_RPAREN, TokenType.MP_EQUAL, TokenType.MP_GTHAN, TokenType.MP_LTHAN, TokenType.MP_GEQUAL, TokenType.MP_LEQUAL, TokenType.MP_NEQUAL, TokenType.MP_PLUS, TokenType.MP_MINUS]
		# and, div, mod, *, / - 92
		if (self.lookAhead.getType() in l1):
			return
		# do, downto, else, end, or, then, to, until - 93
		elif (self.lookAhead.getType() in l2):
			return
		# ',', ;, ), =, >, <, <=, >=, <>, +, '-' - 93
		elif (self.lookAhead.getType() in l3 ):
			return
		else:
			self.error()
		return

	def multiplyingOperator(self):
		# and - 98
		if (self.lookAhead.getType() == TokenType.MP_AND):
			return
		# div - 96
		elif (self.lookAhead.getType() == TokenType.MP_DIV):
			return
		# mod - 97 
		elif (self.lookAhead.getType() == TokenType.MP_MOD):
			return
		# * - 94
		elif (self.lookAhead.getType() == TokenType.MP_TIMES):
			return
		# / - 95
		elif (self.lookAhead.getType() == TokenType.MP_FLOAT_DIVIDE):
			return
		else:
			self.error()
		return

	def factor(self):
		# false - 103
		if (self.lookAhead.getType() == TokenType.MP_FALSE):
			return
		# not - 104
		elif (self.lookAhead.getType() == TokenType.MP_NOT):
			return
		# true - 102
		elif (self.lookAhead.getType() == TokenType.MP_TRUE):
			return
		# id - 106, 116
		elif (self.lookAhead.getType() == TokenType.MP_IDENTIFIER):
			return
		# int_lit - 99
		elif (self.lookAhead.getType() == TokenType.MP_INTEGER_LIT):
			return
		# float_lit - 100
		elif (self.lookAhead.getType() == TokenType.MP_FLOAT_LIT):
			return
		# string_lit - 101
		elif (self.lookAhead.getType() == TokenType.MP_STRING_LIT):
			return
		# ( - 105
		elif (self.lookAhead.getType() == TokenType.MP_LPAREN):
			return
		else:
			self.error()
		return

	def programIdentifier(self):
		# id - 107
		if (self.lookAhead.getType() == TokenType.MP_IDENTIFIER):
			return
		else:
			self.error()
		return

	def variableIdentifier(self):
		# id - 108
		if (self.lookAhead.getType() == TokenType.MP_IDENTIFIER):
			return
		else:
			self.error()
		return

	def procedureIdentifier(self):
		# id - 109
		if (self.lookAhead.getType() == TokenType.MP_IDENTIFIER):
			return
		else:
			self.error()
		return

	def functionIdentifier(self):
		# id - 110
		if (self.lookAhead.getType() == TokenType.MP_IDENTIFIER):
			return
		else:
			self.error()
		return

	def booleanExpression(self):
		l1 = [TokenType.MP_FALSE, TokenType.MP_NOT, TokenType.MP_TRUE, TokenType.MP_IDENTIFIER, TokenType.MP_INTEGER_LIT, TokenType.MP_FLOAT_LIT, TokenType.MP_STRING_LIT, TokenType.MP_LPAREN, TokenType.MP_PLUS, TokenType.MP_MINUS]
		# false, not, true, id, int_lit, float_lit, string_lit, (, +, '-' - 111
		if (self.lookAhead.getType() in l1):
			return
		else:
			self.error()
		return

	def ordinalExpression(self):
		l1 = [TokenType.MP_FALSE, TokenType.MP_NOT, TokenType.MP_TRUE, TokenType.MP_IDENTIFIER, TokenType.MP_INTEGER_LIT, TokenType.MP_FLOAT_LIT, TokenType.MP_STRING_LIT, TokenType.MP_LPAREN, TokenType.MP_PLUS, TokenType.MP_MINUS]
		# false, not, true, id, int_lit, float_lit, string_lit, (, +, '-' - 112
		if (self.lookAhead.getType() in l1):
			return
		else:
			self.error()
		return

	def identifierList(self):
		# id - 113
		if (self.lookAhead.getType() == TokenType.MP_IDENTIFIER):
			return
		else:
			self.error()
		return

	def identifierTail(self):
		# ',' - 114
		if (self.lookAhead.getType() == TokenType.MP_COMMA):
			return
		# : - 115
		elif (self.lookAhead.getType() == TokenType.MP_COLON):
			return
		else:
			self.error()
		return


	def match(self, tokenType):
		if self.lookAhead.getType() == tokenType:
			self.p = self.p + 1
			self.lookAhead =  self.tokens[self.p]
		else:
			self.rror(tokenType)

	def error(self, tokenType):
		t = self.lookAhead
		print("Error at line %s, column %s: expected %s, found %s" % (t.getLineNumber, t.getColumnNumber, tokenType, t.getType()))

