# Lexeme

class Lexeme:
	value = ''

	def __init__(self, in_value):
		self.value = in_value

	def setValue(self, in_value):
		self.value = in_value

	def getValue(self):
		return(self.value)
