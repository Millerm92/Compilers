# Parser
import sys
import Lexeme, Token, TokenTypes, Scanner

def main(argv):
	scanner = Scanner.Scanner()
	scanner.openFile(argv[0])

	flag = False
	i = 0;
	tokens = []
	
	while flag is False:
		token = scanner.getNextToken()
		if token is None:
			flag = True

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

		print("Token: %s, Line %s, Column %s, Lexeme %s, Position %s" % (tokenType, lineNumber, columnNumber, value, position))
			

if __name__ == "__main__":
	main(sys.argv[1:])