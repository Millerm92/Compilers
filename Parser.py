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
		if (self.lookAhead.getType() == TokenType.MP_PROGRAM):
			self.program()
			self.match(TokenType.MP_EOF)
		else:
			self.error(TokenType.MP_EOF)
		return

	def program(self):
		if (self.lookAhead.getType() == TokenType.MP_PROGRAM):
			self.programHeading()
			self.match(TokenType.MP_SCOLON)
			self.block()
		else:
			self.error(TokenType.MP_EOF)
		return

	def programHeading(self):
		if (self.lookAhead.getType() == TokenType.MP_PROGRAM):
			self.match(TokenType.MP_PROGRAM)
			self.programIdentifier()
		else:
			self.error(TokenType.MP_EOF)
		return

	def block(self):
		l = [TokenType.MP_BEGIN, TokenType.MP_FUNCTION, TokenType.MP_PROCEDURE, TokenType.MP_VAR]
		if (self.lookAhead.getType() in l):
			self.variableDeclarationPart()
			self.procedureAndFunctionDeclarationPart()
			self.statementPart()
		else:
			self.error(TokenType.MP_EOF)
		return

	def variableDeclarationPart(self):
		l = [TokenType.MP_BEGIN, TokenType.MP_FUNCTION, TokenType.MP_PROCEDURE]
		if (self.lookAhead.getType() == TokenType.MP_VAR):
			self.match(TokenType.MP_VAR)
			self.variableDeclaration()
			self.match(TokenType.MP_SCOLON)
			self.variableDeclarationTail()
		elif (self.lookAhead.getType() in l):
			return
		else:
			self.error(l)
		return

	def variableDeclarationTail(self):
		l = [TokenType.MP_BEGIN, TokenType.MP_FUNCTION, TokenType.MP_PROCEDURE]
		if (self.lookAhead.getType() == TokenType.MP_IDENTIFIER):
			self.variableDeclaration()
			self.match(TokenType.MP_SCOLON)
			self.variableDeclarationTail()
		elif (self.lookAhead.getType() in l):
			return
		else:
			self.error(l)
		return

	def variableDeclaration(self):
		if(self.lookAhead.getType() == TokenType.MP_IDENTIFIER):
			self.identifierList()
			self.match(TokenType.MP_COLON)
			self.type()
		else:
			self.error(TokenType.MP_IDENTIFIER)
		return

	# HERE
	def type(self):
		l = [TokenType.MP_TRUE, TokenType.MP_FALSE, TokenType.MP_FLOAT, TokenType.MP_INTEGER]
		# HERE HERE HERE HERE mp_boolean vs. mp_true & mp_false?
		if(self.lookAhead.getType() == TokenType.MP_TRUE):
			self.match(TokenType.MP_TRUE)
		elif(self.lookAhead.getType() == TokenType.MP_FALSE):
			self.match(TokenType.MP_FALSE)
		elif(self.lookAhead.getType() == TokenType.MP_FLOAT):
			self.match(TokenType.MP_FLOAT)
		elif(self.lookAhead.getType() == TokenType.MP_INTEGER):
			self.match(TokenType.MP_INTEGER)
		# HERE HERE HERE HERE do i match string_lit or just string?
		elif(self.lookAhead.getType() == TokenType.MP_STRING_LIT):
			self.match(TokenType.MP_STRING_LIT)
		else:
			self.error(l)
		return

	def procedureAndFunctionDeclarationPart(self):
		# begin -16 
		# function - 15
		# procedure - 14
		return

	def procedureDeclaration(self):
		# procedure 17
		return

	def functionDeclaration(self):
		# function 18
		return

	def procedureHeading(self):
		# procedure - 19
		return

	def functionHeading(self):
		# function - 20
		return

	def optionalFormalParameterList(self):
		# ; - 22
		# : - 22
		# ( - 21
		return

	def formalParameterSectionTail(self):
		# ; - 23
		# ) - 24
		return

	def formalParameterSection(self):
		# var - 26
		# id - 25
		return

	def valueParameterSection(self):
		# id - 27
		return

	def variableParameterSection(self):
		# var - 28
		return

	def statementPart(self):
		# begin - 29
		return

	def compoundStatement(self):
		# begin - 30
		return

	def statementSequence(self):
		# begin, end, for, if, read, repeat - 31
		# until, while, write, writeln, id, ; - 31

		return

	def statementTail(self):
		# else, until - 33
		# ; - 32
		return

	def statement(self):
		# begin - 35
		# else, end, until, ; - 34
		# for - 42
		# if - 39
		# procedure 43
		# read - 36
		# repeat - 41
		# while - 40
		# write, writeln - 37
		# id - 38,43
		return

	def emptyStatement(self):
		# else, end, until, ; - 44
		return

	def readStatement(self):
		# read - 45
		return

	def readParameterTail(self):
		# ',' - 46
		# ) - 47
		return

	def readParameter(self):
		# id - 48
		return

	def writeStatement(self):
		# write - 49
		# writeln - 50
		return

	def writeParameterTail(self):
		# ',' - 51
		# ) - 52
		return

	def writeParameter(self):
		# false, not, true, id, int_lit, float_lit, string_lit
		# (, +, '-' - 53
		return

	def assignmentStatement(self):
		# id - 54, 55
		return

	def ifStatement(self):
		# if - 56
		return

	def optionalElsePart(self):
		# else - 57, 58
		# end, until, ; - 58
		return

	def repeatStatement(self):
		# repeat - 59
		return

	def whileStatement(self):
		# while - 60
		return

	def forStatement(self):
		# for - 61
		return

	def controleVariable(self):
		# id - 62
		return

	def initialValue(self):
		# false, not, true, id, int_lit, float_lit, string_lit - 63
		# (, +, '-' - 63
		return

	def stepValue(self):
		# downto - 65
		# to - 64
		return

	def finalValue(self):
		# false, not, true, id, int_lit, float_lit, string_lit - 66
		# (, +, '-' - 66
		return

	def procedureStatement(self):
		# id - 67
		return

	def optionalActualParameterList(self):
		# else, end, until, ; - 69
		# ( - 68
		return

	def actualParameterTail(self):
		# ',' - 70
		# ) - 71
		return

	def actualParameter(self):
		# false, not, true, id, int_lit_float_lit, string_lit - 72
		# (, +, '-' - 72
		return

	def expression(self):
		# false, not, true, id, int_lit, float_lit, string_lit - 73
		# (, +, '-' - 73
		return

	def optionalRelationalPart(self):
		# do, downto, else, end, then, to, until, ',', ;, ( - 75
		# =, >, <, <=, >=, <> - 74
		return

	def relationalOperator(self):
		# = - 76
		# > - 78
		# < - 77
		# <= - 79
		# >= - 80
		# <> - 81
		return

	def simpleExpression(self):
		# false, not, true, id, int_lit, float_lit, string_lit - 82
		# (, +, '-' - 82
		return

	def termTail(self):
		# do, downto, else, end, then, to, until - 84
		# ',', ;, ), =, >, <, <=, >=, <> - 84
		# or, +, '-' - 83
		return

	def optionalSign(self):
		# false, not, true, id, int_lit, float_lit, string_lit, ( - 87
		# +, - 85
		# '-', - 86
		return

	def addingOperator(self):
		# or - 90
		# + - 88
		# '-' - 89
		return

	def term(self):
		# false, not, true, id, int_lit, float_lit, string_lit, ( - 91
		return

	def factorTail(self):
		# and, div, mod, *, / - 92
		# do, downto, else, end, or, then, to, until - 93
		# ',', ;, ), =, >, <, <=, >=, <>, +, '-' - 93
		return

	def multiplyingOperator(self):
		# and - 98
		# div - 96
		# mod - 97 
		# * - 94
		# / - 95
		return

	def factor(self):
		# false - 103
		# not - 104
		# true - 102
		# id - 106, 116
		# int_lit - 99
		# float_lit - 100
		# string_lit - 101
		# ( - 105
		return

	def programIdentifier(self):
		# id - 107
		return

	def variableIdentifier(self):
		# id - 108
		return

	def procedureIdentifier(self):
		# id - 109
		return

	def functionIdentifier(self):
		# id - 110
		return

	def booleanExpression(self):
		# false, not, true, id, int_lit, float_lit, string_lit, (, +, '-' - 111
		return

	def ordinalExpression(self):
		# false, not, true, id, int_lit, float_lit, string_lit, (, +, '-' - 112
		return

	def identifierList(self):
		# id - 113
		return

	def identifierTail(self):
		# ',' - 114
		# : - 115
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

