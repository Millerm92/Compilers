# Scanner

# TODO:
# FIXED_LIT, ERROR
# NEQ
# FIX COMMENTS


import Token, Lexeme
from TokenType import TokenType

class Scanner:
	scanFile = None
	outputFile = None

	line = None
	column = None

	state = 0
	endOfFile = False

	def __init__ (self):
		self.scanFile = None
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

		self.state = 0
		token = None
		lexeme = ''
		startLine = 0
		startColumn = 0
		tType = None

		flag = True
		while flag:
			nextChar = self.scanFile.read(1)
			self.column += 1
			if nextChar == '\n':
				self.newLine()
			elif not nextChar:
				token = Token.Token('EOF', self.line, self.column, TokenType.MP_EOF)
				self.endOfFile = True
				return token
			elif nextChar != ' ':
				startLine = self.line
				startColumn = self.column
				flag = False

		lexeme += nextChar
		nextChar = self.scanFile.read(1)
		self.column += 1

		if not nextChar:
			token = Token.Token('EOF', self.line, self.column, TokenType.MP_EOF)
			self.endOfFile = True
			return token

		# FSA
		flag = True
		first = True
		numLeft = 0
		numRight = 0
		while flag:
			l_0 = [TokenType.MP_ASSIGN, TokenType.MP_GEQUAL, TokenType.MP_LEQUAL, TokenType.MP_NEQUAL]

			# BASE CASE
			if self.state == 0:
				if lexeme.isalpha() or lexeme == "_":
					self.state = 1
				elif lexeme.isdigit():
					self.state = 2
				elif lexeme == '\'':
					self.state = 5
					first = False
				elif lexeme == '{':
					numLeft += 1
					self.state = 7
				else:
					tType = self.checkSingleStringTokens(lexeme, nextChar)
					if tType is not None:
						if tType in l_0:
							lexeme += nextChar
						else:
							self.scanFile.seek(-1, 1)
							self.column -= 1
						token = Token.Token(lexeme, startLine, startColumn, tType)
					else:
						token = Token.Token(lexeme, startLine, startColumn, TokenType.MP_ERROR)
					return token

			# IDENTIFIERS/RESERVED WORDS
			if self.state == 1:
				if not nextChar or not (nextChar.isalpha() or nextChar.isdigit() or nextChar == '_'):
					if lexeme == '_':
						token = Token.Token(lexeme, startLine, startColumn, TokenType.MP_ERROR)
						self.scanFile.seek(-1, 1)
						self.column -= 1
						return token
					self.scanFile.seek(-1, 1)
					self.column -= 1
					
					tType = self.checkReservedWords(lexeme)
					if tType is None:
						token = Token.Token(lexeme, startLine, startColumn, TokenType.MP_IDENTIFIER)
					else:
						token = Token.Token(lexeme, startLine, startColumn, tType)
					return token
				else: 
					lexeme += nextChar


			# MATHEMATICAL LITERALS
			# Integer
			elif self.state == 2:
				if first:
					if lexeme == '0' and nextChar.isdigit():
						token = Token.Token(lexeme, startLine, startColumn, TokenType.MP_ERROR)
						self.scanFile.seek(-1, 1)
						self.column -= 1
						return token
					else:
						first = False
				if nextChar.isdigit():
					lexeme += nextChar
				elif nextChar == '.':
					self.state = 3
					lexeme += nextChar
				elif nextChar.lower() == 'e':
					first = True
					self.state = 4
					lexeme += nextChar
				else:
					token = Token.Token(lexeme, startLine, startColumn, TokenType.MP_INTEGER_LIT)
					self.scanFile.seek(-1, 1)
					self.column -= 1
					return token
			# Fixed
			elif self.state == 3:
				if nextChar.isdigit():
					lexeme += nextChar
				elif nextChar.lower() == 'e':
					first = True
					self.state = 4
					lexeme += nextChar
				else:
					if nextChar.isalpha():
						token = Token.Token(lexeme, startLine, startColumn, TokenType.MP_ERROR)
					else:
						token = Token.Token(lexeme, startLine, startColumn, TokenType.MP_FIXED_LIT)
					self.scanFile.seek(-1, 1)
					self.column -= 1
					return token
			# Float
			elif self.state == 4:
				if first:
					first = False
					if nextChar == '+' or nextChar == '-':
						lexeme += nextChar
					else:
						token = Token.Token(lexeme, startLine, startColumn, TokenType.MP_ERROR)
						return token
				else:
					if nextChar.isdigit():
						lexeme += nextChar
					else:
						if (nextChar.isalpha()):
							token = Token.Token(lexeme, startLine, startColumn, TokenType.MP_ERROR)
						else:
							token = Token.Token(lexeme, startLine, startColumn, TokenType.MP_FLOAT_LIT)
						self.scanFile.seek(-1, 1)
						self.column -= 1
						return token

			# STRING
			elif self.state == 5:
				if nextChar == '\'':
					self.state = 6
				else:
					if not nextChar or nextChar == '\n':
						token = Token.Token(lexeme, startLine, startColumn, TokenType.MP_ERROR)
						self.scanFile.seek(-1, 1)
						self.column -= 1
						return token
				lexeme += nextChar
			elif self.state == 6:
				if nextChar == '\'':
					lexeme += nextChar
					self.state = 5
				else:
					token = Token.Token(lexeme, startLine, startColumn, TokenType.MP_STRING_LIT)
					self.scanFile.seek(-1, 1)
					self.column -= 1
					return token

			# COMMENTS
			elif self.state == 7:
				if numLeft == numRight:
					token = Token.Token(lexeme, startLine, startColumn, TokenType.MP_RUN_COMMENT)
					self.scanFile.seek(-1, 1)
					self.column -= 1
					return token
				else:
					if not nextChar:
						token = Token.Token(lexeme, startLine, startColumn, TokenType.MP_ERROR)
						self.scanFile.seek(-1, 1)
						self.column -= 1
						return token
					elif nextChar == '{':
						numLeft += 1
					elif nextChar == '}':
						numRight += 1
					lexeme += nextChar




			nextChar = self.scanFile.read(1)
			self.column += 1



	def checkSingleStringTokens(self, inLexeme, nextChar):
		literal = inLexeme.lower()
		tType = None

		if literal == ":" and nextChar == '=':
			tType = TokenType.MP_ASSIGN
		elif literal == ":":
			tType = TokenType.MP_COLON
		elif literal == ",":
			tType = TokenType.MP_COMMA
		elif literal == "=":
			tType = TokenType.MP_EQUAL
		elif literal == "/":
			tType = TokenType.MP_FLOAT_DIVIDE
		elif literal == ">" and nextChar == '=':
			tType = TokenType.MP_GEQUAL
		elif literal == ">":
			tType = TokenType.MP_GTHAN
		elif literal == "<" and nextChar == '=':
			tType = TokenType.MP_LEQUAL
		elif literal == "(":
			tType = TokenType.MP_LPAREN
		elif literal == "<":
			tType = TokenType.MP_LTHAN
		elif literal == "-":
			tType = TokenType.MP_MINUS
		elif literal == "<" and nextChar == '>':
			tType = TokenType.MP_NEQUAL
		elif literal == ".":
			tType = TokenType.MP_PERIOD
		elif literal == "+":
			tType = TokenType.MP_PLUS
		elif literal == ")":
			tType = TokenType.MP_RPAREN
		elif literal == ";":
			tType = TokenType.MP_SCOLON
		elif literal == "*":
			tType = TokenType.MP_TIMES

		return tType


	def checkReservedWords(self, inLexeme):
		literal = inLexeme.lower()
		tType = None
			
		if literal == 'and':
			tType = TokenType.MP_AND
		elif literal == 'begin':
			tType = TokenType.MP_BEGIN
		elif literal == 'div':
			tType = TokenType.MP_DIV
		elif literal == 'do':
			tType = TokenType.MP_DO
		elif literal == 'downto':
			tType = TokenType.MP_DOWNTO
		elif literal == 'else':
			tType = TokenType.MP_ELSE
		elif literal == 'end':
			tType = TokenType.MP_END
		elif literal == 'false':
			tType = TokenType.MP_FALSE
		elif literal == 'fixed':
			tType = TokenType.MP_FIXED
		elif literal == 'float':
			tType = TokenType.MP_FLOAT
		elif literal == 'for':
			tType = TokenType.MP_FOR
		elif literal == 'function':
			tType = TokenType.MP_FUNCTION
		elif literal == 'if':
			tType = TokenType.MP_IF
		elif literal == 'integer':
			tType = TokenType.MP_INTEGER
		elif literal == 'mod':
			tType = TokenType.MP_MOD
		elif literal == 'not':
			tType = TokenType.MP_NOT
		elif literal == 'or':
			tType = TokenType.MP_OR
		elif literal == 'procedure':
			tType = TokenType.MP_PROCEDURE
		elif literal == 'program':
			tType = TokenType.MP_PROGRAM
		elif literal == 'read':
			tType = TokenType.MP_READ
		elif literal == 'repeat':
			tType = TokenType.MP_REPEAT
		elif literal == 'string':
			tType = TokenType.MP_STRING
		elif literal == 'then':
			tType = TokenType.MP_THEN
		elif literal == 'true':
			tType = TokenType.MP_TRUE
		elif literal == 'to':
			tType = TokenType.MP_TO
		elif literal == 'until':
			tType = TokenType.MP_UNTIL
		elif literal == 'var':
			tType = TokenType.MP_VAR
		elif literal == 'while':
			tType = TokenType.MP_WHILE
		elif literal == 'write':
			tType = TokenType.MP_WRITE
		elif literal == 'writeln':
			tType = TokenType.MP_WRITELN

		return tType