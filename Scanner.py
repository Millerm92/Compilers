# Scanner
import Token, Lexeme
from TokenType import TokenType

class Scanner:
	scanFile = None
	outputFile = None

	line = None
	column = None

	endOfFile = False

	def __init__ (self):
		self.scanFile = None
		self.outputFile = open('output.txt', 'w')
		self.line = 1
		self.column = 1

	def openFile(self, inFile):
		self.scanFile = open(inFile)

	def newLine(self):
		self.line += 1
		self.column = 1

	def getNextToken(self):
		if self.endOfFile is True:
			return None

		thisToken = Token.Token(self.line, self.column)
		nextChar = self.scanFile.read(1)
		lexeme = ''
		self.column += 1
		flag = False

		while not flag:
			if nextChar == ' ':
				self.column += 1
				return None
			elif nextChar == '\n':
				self.newLine()
				return None
			elif not nextChar:
				thisToken.setLexeme("EOF")
				thisToken.setLexeme(TokenType.MP_EOF)
				self.endOfFile = True
				return thisToken
			else:
				lexeme += nextChar

			nextChar = self.scanFile.read(1)
			if nextChar == '\n':
				self.newLine()
			else:
				self.column += 1

			# CHECK SINGLE STRING TOKENS
			if len(lexeme) <= 3:
				res = self.checkSingleStringTokens(lexeme, thisToken, nextChar)
				if res is True:
					return thisToken

			# CHECK RESERVED WORDS
			res = self.checkReservedWords(lexeme, thisToken, nextChar)
			if res is True:
				return thisToken


	def checkSingleStringTokens(self, inLexeme, inToken, nextChar):
		literal = inLexeme.lower()

		if literal == ":" and nextChar == '=':
			inToken.setLexeme(":=")
			inToken.setType(TokenType.MP_ASSIGN)
			return True
		elif literal == ":":
			inToken.setLexeme(inLexeme)
			inToken.setType(TokenType.MP_COLON)
			return True
		elif literal == ",":
			inToken.setLexeme(inLexeme)
			inToken.setType(TokenType.MP_COMMA)
			return True
		elif literal == "=":
			inToken.setLexeme(inLexeme)
			inToken.setType(TokenType.MP_EQUAL)
			return True
		elif literal == "/":
			inToken.setLexeme(inLexeme)
			inToken.setType(TokenType.MP_FLOAT_DIVIDE)
			return True
		elif literal == ">" and nextChar == '=':
			inToken.setLexeme(">=")
			inToken.setType(TokenType.MP_GEQUAL)
			return True
		elif literal == ">":
			inToken.setLexeme(inLexeme)
			inToken.setType(TokenType.MP_GTHAN)
			return True
		elif literal == "<" and nextChar == '=':
			inToken.setLexeme("<=")
			inToken.setType(TokenType.MP_LEQUAL)
			return True
		elif literal == "(":
			inToken.setLexeme(inLexeme)
			inToken.setType(TokenType.MP_LPAREN)
			return True
		elif literal == "<":
			inToken.setLexeme(inLexeme)
			inToken.setType(TokenType.MP_LTHAN)
			return True
		elif literal == "-":
			inToken.setLexeme(inLexeme)
			inToken.setType(TokenType.MP_MINUS)
			return True
		elif literal == "!" and nextChar == '=':
			inToken.setLexeme("!=")
			inToken.setType(TokenType.MP_NEQUAL)
			return True
		elif literal == ".":
			inToken.setLexeme(inLexeme)
			inToken.setType(TokenType.MP_PERIOD)
			return True
		elif literal == "+":
			inToken.setLexeme(inLexeme)
			inToken.setType(TokenType.MP_PLUS)
			return True
		elif literal == ")":
			inToken.setLexeme(inLexeme)
			inToken.setType(TokenType.MP_RPAREN)
			return True
		elif literal == ";":
			inToken.setLexeme(inLexeme)
			inToken.setType(TokenType.MP_SCOLON)
			return True
		elif literal == "*":
			inToken.setLexeme(inLexeme)
			inToken.setType(TokenType.MP_TIMES)
			return True
		else:
			return False


	def checkReservedWords(self, inLexeme, inToken, nextChar):
		literal = inLexeme.lower()
		if nextChar == ' ' or nextChar == '\n' or not nextChar:
			if literal == 'and':
				inToken.setLexeme(inLexeme)
				inToken.setType(TokenType.MP_AND)
				return True
			elif literal == 'begin':
				inToken.setLexeme(inLexeme)
				inToken.setType(TokenType.MP_BEGIN)
				return True
			elif literal == 'div':
				inToken.setLexeme(inLexeme)
				inToken.setType(TokenType.MP_DIV)
				return True
			elif literal == 'do':
				inToken.setLexeme(inLexeme)
				inToken.setType(TokenType.MP_DO)
				return True
			elif literal == 'downto':
				inToken.setLexeme(inLexeme)
				inToken.setType(TokenType.MP_DOWNTO)
				return True
			elif literal == 'else':
				inToken.setLexeme(inLexeme)
				inToken.setType(TokenType.MP_ELSE)
				return True
			elif literal == 'end':
				inToken.setLexeme(inLexeme)
				inToken.setType(TokenType.MP_END)
				return True
			elif literal == 'false':
				inToken.setLexeme(inLexeme)
				inToken.setType(TokenType.MP_FALSE)
				return True
			elif literal == 'fixed':
				inToken.setLexeme(inLexeme)
				inToken.setType(TokenType.MP_FIXED)
				return True
			elif literal == 'float':
				inToken.setLexeme(inLexeme)
				inToken.setType(TokenType.MP_FLOAT)
				return True
			elif literal == 'for':
				inToken.setLexeme(inLexeme)
				inToken.setType(TokenType.MP_FOR)
				return True
			elif literal == 'function':
				inToken.setLexeme(inLexeme)
				inToken.setType(TokenType.MP_FUNCTION)
				return True
			elif literal == 'if':
				inToken.setLexeme(inLexeme)
				inToken.setType(TokenType.MP_IF)
				return True
			elif literal == 'integer':
				inToken.setLexeme(inLexeme)
				inToken.setType(TokenType.MP_INTEGER)
				return True
			elif literal == 'mod':
				inToken.setLexeme(inLexeme)
				inToken.setType(TokenType.MP_MOD)
				return True
			elif literal == 'not':
				inToken.setLexeme(inLexeme)
				inToken.setType(TokenType.MP_NOT)
				return True
			elif literal == 'or':
				inToken.setLexeme(inLexeme)
				inToken.setType(TokenType.MP_OR)
				return True
			elif literal == 'procedure':
				inToken.setLexeme(inLexeme)
				inToken.setType(TokenType.MP_PROCEDURE)
				return True
			elif literal == 'program':
				inToken.setLexeme(inLexeme)
				inToken.setType(TokenType.MP_PROGRAM)
				return True
			elif literal == 'read':
				inToken.setLexeme(inLexeme)
				inToken.setType(TokenType.MP_READ)
				return True
			elif literal == 'repeat':
				inToken.setLexeme(inLexeme)
				inToken.setType(TokenType.MP_REPEAT)
				return True
			elif literal == 'string':
				inToken.setLexeme(inLexeme)
				inToken.setType(TokenType.MP_STRING)
				return True
			elif literal == 'then':
				inToken.setLexeme(inLexeme)
				inToken.setType(TokenType.MP_THEN)
				return True
			elif literal == 'true':
				inToken.setLexeme(inLexeme)
				inToken.setType(TokenType.MP_TRUE)
				return True
			elif literal == 'to':
				inToken.setLexeme(inLexeme)
				inToken.setType(TokenType.MP_TO)
				return True
			elif literal == 'until':
				inToken.setLexeme(inLexeme)
				inToken.setType(TokenType.MP_UNTIL)
				return True
			elif literal == 'var':
				inToken.setLexeme(inLexeme)
				inToken.setType(TokenType.MP_VAR)
				return True
			elif literal == 'while':
				inToken.setLexeme(inLexeme)
				inToken.setType(TokenType.MP_WHILE)
				return True
			elif literal == 'write':
				inToken.setLexeme(inLexeme)
				inToken.setType(TokenType.MP_WRITE)
				return True
			elif literal == 'writeln':
				inToken.setLexeme(inLexeme)
				inToken.setType(TokenType.MP_WRITELN)
				return True
			else:
				return False
		else:
			return False
		

