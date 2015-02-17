# Parser
import sys
import Lexeme, Token, TokenTypes, Scanner

def main(argv):
	scanner = Scanner.Scanner()
	scanner.openFile(argv[0])

	flag = False

	while flag is False:
		token = scanner.getNextToken()
		if token is None:
			flag = True

		if flag is False:
			tokenType = token.getType()
			lineNumber = token.getLineNumber()
			columnNumber = token.getColumnNumber()
			value = token.getLexeme().getValue()

			print("Token: %s, Line %s, Column %s, Lexeme %s" % (tokenType, lineNumber, columnNumber, value))

if __name__ == "__main__":
	main(sys.argv[1:])