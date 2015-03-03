# token
import Lexeme
from TokenType import TokenType

class Token:
	lineNumber = None
	columnNumber = None
	lexeme = None
	lexemeNumber = None
	data = None
	tokenType = None


	def __init__(self, inLineNum, inColumnNum):
		self.lineNumber = inLineNum
		self.columnNumber = inColumnNum

	def setType(self, inTokenType):
		self.tokenType = inTokenType

	def getType(self):
		return(self.tokenType)

	def setLexeme(self, inValue):
		thisLexeme = Lexeme.Lexeme(inValue)
		self.lexeme = thisLexeme

	def getLexeme(self):
		return(self.lexeme)

	def getLineNumber(self):
		return(self.lineNumber)

	def getColumnNumber(self):
		return(self.columnNumber)
		
