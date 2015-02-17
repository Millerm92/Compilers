# Scanner
import Token, Lexeme, TokenTypes

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
		startIndex = self.column
		flag = False

		while not flag:
			nextChar = self.scanFile.read(1)
			if not nextChar:
				flag = True
				self.endOfFile = True
			elif nextChar == ' ':
				flag = True
			elif nextChar == '\n':
				self.line += 1
				self.column = 0
				flag = True
			else:
				lexeme = lexeme + nextChar
			self.column += 1

		thisLexeme = Lexeme.Lexeme(lexeme)
		
		
		#
		#Determine TokenType
		#
		
		tokenType = -1;
		
		if lexeme == 'int':
			tokenType = 6
		elif lexeme == 'denbigh':
			tokenType = 8
		elif lexeme == '=':
			tokenType = 4
		elif lexeme == '4':
			tokenType = 1
		elif lexeme == ';':
			tokenType = 7
		elif lexeme == '+':
			tokenType = 4
		elif lexeme == '1':
			tokenType = 1
		else:
			tokenType = -1
		
		#
		#
		#
		
		
		thisToken = Token.Token(self.line, startIndex, thisLexeme, tokenType)
		return thisToken


	def determineTokenType(self):
		return -1
		

