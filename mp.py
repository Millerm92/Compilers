# Parser
import sys
import Lexeme, Token, Scanner, Parser
from TokenType import TokenType

def main(argv):

	scanner = Scanner.Scanner()
	scanner.openFile(argv[0])

	parser = Parser.Parser()

	flag = False

	while flag is False:
		token = scanner.getNextToken()

		if (token.getType() != TokenType.MP_RUN_COMMENT):
			parser.addToken(token)

		if token.getType() == TokenType.MP_EOF:
			flag = True

	parser.printTokens()
	parser.checkGrammar()


if __name__ == "__main__":
	main(sys.argv[1:])