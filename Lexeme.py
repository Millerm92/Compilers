# Lexeme

class Lexeme:
	value = ''

	def __init__(self, inValue):
		self.value = inValue

	def setValue(self, inValue):
		self.value = inValue

	def getValue(self):
		return(self.value)
