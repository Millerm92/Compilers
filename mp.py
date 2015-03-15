# Parser
import sys
import Lexeme, Token, Scanner
from TokenType import TokenType

def main(argv):
	scanner = Scanner.Scanner()
	scanner.openFile(argv[0])

	flag = False
	
	while flag is False:
		token = scanner.getNextToken()

		if token != None:

			tokenType = token.getType()
			lineNumber = token.getLineNumber()
			columnNumber = token.getColumnNumber()
			lexeme = token.getLexeme().getValue()

			print('Token: %s, Line %s, Column %s, Lexeme "%s"' % (tokenType, lineNumber, columnNumber, lexeme))

			if token.getType() == TokenType.MP_EOF:
				flag = True


if __name__ == "__main__":
	main(sys.argv[1:])