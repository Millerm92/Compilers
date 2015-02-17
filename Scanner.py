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
		thisToken = Token.Token(self.line, startIndex, thisLexeme)

		return thisToken


	def determineTokenType(self):
		return -1
		

