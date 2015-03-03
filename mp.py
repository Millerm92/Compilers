# Parser
import sys
import Lexeme, Token, Scanner
from TokenType import TokenType

def main(argv):
	scanner = Scanner.Scanner()
	scanner.openFile(argv[0])

	flag = False
	i = 0;
	tokens = []
	
	while flag is False:
		token = scanner.getNextToken()

<<<<<<< HEAD
		if token is not None:
			tokenType = token.getType()
			lineNumber = token.getLineNumber()
			columnNumber = token.getColumnNumber()
			value = token.getLexeme().getValue()
=======
		if flag is False:
			tokens.append(token)
			token.position = i;
			i = i + 1
			
	for i in range(len(tokens)):
		token = tokens[i]
		
		tokenType = token.getType()
		lineNumber = token.getLineNumber()
		columnNumber = token.getColumnNumber()
		value = token.getLexeme().getValue()
		position = token.getPosition()
>>>>>>> 3826951d3a366aa9c5418b2a3ca0dcb8514e3e68

		print("Token: %s, Line %s, Column %s, Lexeme %s, Position %s" % (tokenType, lineNumber, columnNumber, value, position))
			

			if token.getType() == TokenType.MP_EOF:
				flag = True

if __name__ == "__main__":
	main(sys.argv[1:])