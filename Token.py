# token
import Lexeme, TokenTypes

class Token:
	lexeme = None
	lineNumber = None
	columnNumber = None
	lexeme = None
	lexemeNumber = None
	data = None
	tokenType = None

	def __init__(self, in_line_num, in_column_num, in_lexeme):
		self.lineNumber = in_line_num
		self.columnNumber = in_column_num
		self.lexeme = in_lexeme

	def getType(self):
		#return(self.tokenType)
		return("TBD")

	def getLexeme(self):
		return(self.lexeme)

	def getLineNumber(self):
		return(self.lineNumber)

	def getColumnNumber(self):
		return(self.columnNumber)


	# Determine what type of token i am based on my global lexeme literal
	# by sending the lexeme to a series of FSAs, if an FSA returns true
	# than we know to break out of this function as the call to that FSA
	# will have changed the global tokenType AND lexemeNumber.
	def determineType():
		return None
