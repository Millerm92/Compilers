# PARSER
import sys
import Lexeme, Token, Scanner
from TokenType import TokenType

class Parser:
	tokens = []
	lookAhead = None
	p = 0

	def __init__(self):
		tokens = []
		lookAhead = None
		p = 0

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
			self.error()

		return


	def match(self, tokenType):
		if self.lookAhead.getType() == tokenType:
			self.p = self.p + 1
			self.lookAhead =  self.tokens[self.p]
		else:
			error(tokenType)

	def error(self, tokenType):
		t = self.lookAhead
		print("Error at line %s, column %s: expected %s, found %s" % (t.getLineNumber, t.getColumnNumber, tokenType, t.getType()))

