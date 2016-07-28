##############################################################################
# Copyright (c) 2013-2016, Lawrence Livermore National Security, LLC.
# Produced at the Lawrence Livermore National Laboratory.
#
# This file is part of Spack.
# Created by Todd Gamblin, tgamblin@llnl.gov, All rights reserved.
# LLNL-CODE-647188
#
# For details, see https://github.com/llnl/spack
# Please also see the LICENSE file for our notice and the LGPL.
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License (as
# published by the Free Software Foundation) version 2.1, February 1999.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the IMPLIED WARRANTY OF
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the terms and
# conditions of the GNU Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public
# License along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA 02111-1307 USA
##############################################################################
import re
import itertools
import spack.error


class Token:
    """Represents tokens; generated from input by lexer and fed to parse()."""
    def __init__(self, type, value='', start=0, end=0):
        self.type = type
        self.value = value
        self.start = start
        self.end = end

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
        return Token(type, value, self.scanner.match.start(0), self.scanner.match.end(0))

    def lex(self, text):
        tokens, remainder = self.scanner.scan(text)
        if remainder:
            raise LexError("Invalid character", text, text.index(remainder))
        return tokens


class Parser(object):
    """Base class for simple recursive descent parsers."""
    def __init__(self, lexer):
        self.tokens = iter([])   # iterators over tokens, handled in order.  Starts empty.
        self.token = Token(None) # last accepted token starts at beginning of file
        self.next = None         # next token
        self.lexer = lexer
        self.text = None

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

    def next_token_error(self, message):
        """Raise an error about the next token in the stream."""
        raise ParseError(message, self.text, self.token.end)

    def last_token_error(self, message):
        """Raise an error about the previous token in the stream."""
        raise ParseError(message, self.text, self.token.start)

    def unexpected_token(self):
        self.next_token_error("Unexpected token")

    def expect(self, id):
        """Like accept(), but fails if we don't like the next token."""
        if self.accept(id):
            return True
        else:
            if self.next:
                self.unexpected_token()
            else:
                self.next_token_error("Unexpected end of input")
            sys.exit(1)

    def setup(self, text):
        self.text = text
        self.push_tokens(self.lexer.lex(text))

    def parse(self, text):
        self.setup(text)
        return self.do_parse()



class ParseError(spack.error.SpackError):
    """Raised when we don't hit an error while parsing."""
    def __init__(self, message, string, pos):
        super(ParseError, self).__init__(message)
        self.string = string
        self.pos = pos


class LexError(ParseError):
    """Raised when we don't know how to lex something."""
    def __init__(self, message, string, pos):
        super(LexError, self).__init__(message, string, pos)
