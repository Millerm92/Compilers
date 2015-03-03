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
		self.column = 0

	def openFile(self, inFile):
		self.scanFile = open(inFile)

	def newLine(self):
		self.line += 1
		self.column = 0

	def getNextToken(self):
		if self.endOfFile is True:
			return None

		lexeme = ''
		thisToken = Token.Token(self.line, self.column)

		flag = False
		nextChar = self.scanFile.read(1)

		while not flag:
			charAfter = self.scanFile.read(1)

			if not nextChar:
				thisToken.setLexeme("EOF")
				thisToken.setType(TokenType.MP_EOF)
				flag = True
				self.endOfFile = True
			elif nextChar == ' ':
				flag = True
			elif nextChar == '\n':
				self.newLine()
				flag = True

			lexeme = lexeme + nextChar
			
			self.column += 1
			nextChar = charAfter

			# CHECK SINGLE STRING TOKENS
			if len(lexeme) <= 3 and lexeme != ' ':
				res = self.checkSingleStringTokens(lexeme, thisToken, nextChar)
				if res is True:
					return thisToken

			# CHECK RESERVED WORDS
			if lexeme != ' ':
				res = self.checkReservedWords(lexeme, thisToken, nextChar)
				if res is True:
					return thisToken

		

		if lexeme != ' ':
			thisToken.setType(TokenType.UNDEFINED)
			thisToken.setLexeme("UNDEFINED")
			return thisToken

		return None


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

		if literal == 'and' and nextChar == ' ':
			inToken.setLexeme(inLexeme)
			inToken.setType(TokenType.MP_AND)
			return True
		elif literal == 'begin' and nextChar == ' ':
			inToken.setLexeme(inLexeme)
			inToken.setType(TokenType.MP_BEGIN)
			return True
		elif literal == 'div' and nextChar == ' ':
			inToken.setLexeme(inLexeme)
			inToken.setType(TokenType.MP_DIV)
			return True
		elif literal == 'do' and nextChar == ' ':
			inToken.setLexeme(inLexeme)
			inToken.setType(TokenType.MP_DO)
			return True
		elif literal == 'downto' and nextChar == ' ':
			inToken.setLexeme(inLexeme)
			inToken.setType(TokenType.MP_DOWNTO)
			return True
		elif literal == 'else' and nextChar == ' ':
			inToken.setLexeme(inLexeme)
			inToken.setType(TokenType.MP_ELSE)
			return True
		elif literal == 'end' and nextChar == ' ':
			inToken.setLexeme(inLexeme)
			inToken.setType(TokenType.MP_END)
			return True
		elif literal == 'false' and nextChar == ' ':
			inToken.setLexeme(inLexeme)
			inToken.setType(TokenType.MP_FALSE)
			return True
		elif literal == 'fixed' and nextChar == ' ':
			inToken.setLexeme(inLexeme)
			inToken.setType(TokenType.MP_FIXED)
			return True
		elif literal == 'float' and nextChar == ' ':
			inToken.setLexeme(inLexeme)
			inToken.setType(TokenType.MP_FLOAT)
			return True
		elif literal == 'for' and nextChar == ' ':
			inToken.setLexeme(inLexeme)
			inToken.setType(TokenType.MP_FOR)
			return True
		elif literal == 'function' and nextChar == ' ':
			inToken.setLexeme(inLexeme)
			inToken.setType(TokenType.MP_FUNCTION)
			return True
		elif literal == 'if' and nextChar == ' ':
			inToken.setLexeme(inLexeme)
			inToken.setType(TokenType.MP_IF)
			return True
		elif literal == 'integer' and nextChar == ' ':
			inToken.setLexeme(inLexeme)
			inToken.setType(TokenType.MP_INTEGER)
			return True
		elif literal == 'mod' and nextChar == ' ':
			inToken.setLexeme(inLexeme)
			inToken.setType(TokenType.MP_MOD)
			return True
		elif literal == 'not' and nextChar == ' ':
			inToken.setLexeme(inLexeme)
			inToken.setType(TokenType.MP_NOT)
			return True
		elif literal == 'or' and nextChar == ' ':
			inToken.setLexeme(inLexeme)
			inToken.setType(TokenType.MP_OR)
			return True
		elif literal == 'procedure' and nextChar == ' ':
			inToken.setLexeme(inLexeme)
			inToken.setType(TokenType.MP_PROCEDURE)
			return True
		elif literal == 'program' and nextChar == ' ':
			inToken.setLexeme(inLexeme)
			inToken.setType(TokenType.MP_PROGRAM)
			return True
		elif literal == 'read' and nextChar == ' ':
			inToken.setLexeme(inLexeme)
			inToken.setType(TokenType.MP_READ)
			return True
		elif literal == 'repeat' and nextChar == ' ':
			inToken.setLexeme(inLexeme)
			inToken.setType(TokenType.MP_REPEAT)
			return True
		elif literal == 'string' and nextChar == ' ':
			inToken.setLexeme(inLexeme)
			inToken.setType(TokenType.MP_STRING)
			return True
		elif literal == 'then' and nextChar == ' ':
			inToken.setLexeme(inLexeme)
			inToken.setType(TokenType.MP_THEN)
			return True
		elif literal == 'true' and nextChar == ' ':
			inToken.setLexeme(inLexeme)
			inToken.setType(TokenType.MP_TRUE)
			return True
		elif literal == 'to' and nextChar == ' ':
			inToken.setLexeme(inLexeme)
			inToken.setType(TokenType.MP_TO)
			return True
		elif literal == 'until' and nextChar == ' ':
			inToken.setLexeme(inLexeme)
			inToken.setType(TokenType.MP_UNTIL)
			return True
		elif literal == 'var' and nextChar == ' ':
			inToken.setLexeme(inLexeme)
			inToken.setType(TokenType.MP_VAR)
			return True
		elif literal == 'while' and nextChar == ' ':
			inToken.setLexeme(inLexeme)
			inToken.setType(TokenType.MP_WHILE)
			return True
		elif literal == 'write' and nextChar == ' ':
			inToken.setLexeme(inLexeme)
			inToken.setType(TokenType.MP_WRITE)
			return True
		elif literal == 'writeln' and nextChar == ' ':
			inToken.setLexeme(inLexeme)
			inToken.setType(TokenType.MP_WRITELN)
			return True
		else:
			return False
		

