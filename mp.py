import sys
import Token, Scanner, Parser
from TokenType import TokenType

def main(argv):
    scanner = Scanner.Scanner()
    scanner.openFile(argv[0])

    parser = Parser.Parser()
    flag = False

    while flag is False:
        token = scanner.getNextToken()
        if token is not None:
            if token.getType() == TokenType.MP_EOF:
                flag = True

            if not (token.getType() == TokenType.MP_RUN_COMMENT or token.getType() == TokenType.MP_ERROR):
                parser.addToken(token)
        else:
            flag = True

    parser.checkGrammar()

if __name__ == "__main__":
    main(sys.argv[1:])
