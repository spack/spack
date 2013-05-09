import re
import spack.error as err
import itertools

class UnlexableInputError(err.SpackError):
    """Raised when we don't know how to lex something."""
    def __init__(self, message):
        super(UnlexableInputError, self).__init__(message)


class ParseError(err.SpackError):
    """Raised when we don't hit an error while parsing."""
    def __init__(self, message):
        super(ParseError, self).__init__(message)


class Token:
    """Represents tokens; generated from input by lexer and fed to parse()."""
    def __init__(self, type, value=''):
        self.type = type
        self.value = value

    def __repr__(self):
        return str(self)

    def __str__(self):
        return "'%s'" % self.value

    def is_a(self, type):
        return self.type == type

    def __cmp__(self, other):
        return cmp((self.type, self.value),
                   (other.type, other.value))

class Lexer(object):
    """Base class for Lexers that keep track of line numbers."""
    def __init__(self, lexicon):
        self.scanner = re.Scanner(lexicon)

    def token(self, type, value=''):
        return Token(type, value)

    def lex(self, text):
        tokens, remainder = self.scanner.scan(text)
        if remainder:
            raise UnlexableInputError("Unlexable input:\n%s\n" % remainder)
        return tokens


class Parser(object):
    """Base class for simple recursive descent parsers."""
    def __init__(self, lexer):
        self.tokens = iter([]) # iterators over tokens, handled in order.  Starts empty.
        self.token = None      # last accepted token
        self.next = None       # next token
        self.lexer = lexer

    def gettok(self):
        """Puts the next token in the input stream into self.next."""
        try:
            self.next = self.tokens.next()
        except StopIteration:
            self.next = None

    def push_tokens(self, iterable):
        """Adds all tokens in some iterable to the token stream."""
        self.tokens = itertools.chain(iter(iterable), iter([self.next]), self.tokens)
        self.gettok()

    def accept(self, id):
        """Puts the next symbol in self.token if we like it.  Then calls gettok()"""
        if self.next and self.next.is_a(id):
            self.token = self.next
            self.gettok()
            return True
        return False

    def unexpected_token(self):
        raise ParseError("Unexpected token: %s." % self.next)

    def expect(self, id):
        """Like accept(), but fails if we don't like the next token."""
        if self.accept(id):
            return True
        else:
            if self.next:
                self.unexpected_token()
            else:
                raise ParseError("Unexpected end of file.")
            sys.exit(1)

    def parse(self, text):
        self.push_tokens(self.lexer.lex(text))
        return self.do_parse()
