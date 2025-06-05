# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
"""This module provides building blocks for tokenizing strings. Users can define tokens by
inheriting from TokenBase and defining tokens as ordered enum members. The Tokenizer class can then
be used to iterate over tokens in a string."""
import enum
import re
from typing import Generator, Match, Optional, Type


class TokenBase(enum.Enum):
    """Base class for an enum type with a regex value"""

    def __new__(cls, *args, **kwargs):
        value = len(cls.__members__) + 1
        obj = object.__new__(cls)
        obj._value_ = value
        return obj

    def __init__(self, regex):
        self.regex = regex

    def __str__(self):
        return f"{self._name_}"


class Token:
    """Represents tokens; generated from input by lexer and fed to parse()."""

    __slots__ = "kind", "value", "start", "end", "subvalues"

    def __init__(self, kind: TokenBase, value: str, start: int = 0, end: int = 0):
        self.kind = kind
        self.value = value
        self.start = start
        self.end = end
        self.subvalues = None

    def __repr__(self):
        return str(self)

    def __str__(self):
        return f"({self.kind}, {self.value})"

    def __eq__(self, other):
        return (
            self.kind == other.kind
            and self.value == other.value
            and self.subvalues == other.subvalues
        )


def rewrite_subvalues(token: Token, regex: str):
    """Extract named capture groups from the provided regex and prefix them with token name.

    Returns:
        The rewritten regex and a list of pairs mapping subvalue name to rewritten name.
    """
    pairs = []

    def replace(m: MatchObject):
        subvalue_name = m.group(1)
        pairs.append((token.name, subvalue_name))
        return f"(?P<{token.name}_{subvalue_name}>"

    return re.sub(r"\(\?P<([^>]+)>", replace, token.regex), pairs


class Tokenizer:
    def __init__(self, tokens: Type[TokenBase]):
        self.tokens = tokens

        # tokens can have named subexpressions, if their regexes define named capture groups.
        # record this so we can associate them with the token
        self.token_subvalues = {}

        parts = []
        for token in tokens:
            regex = re.sub(
                r"\(\?P<([^>]+)>",
                lambda m: m.replace(m.group(1), f"{token.name}_{m.group(1)}", token.regex),
            )

            subgroups = re.findall(r"\(\?P<([^>]+)>", token.regex)

            parts.append(f"(?P<{token}>{token.regex})")

        for token in tokens:

            if subgroups:
                self.token_subvalues[token.name] = subgroups

        print(self.token_subvalues)

        self.regex = re.compile("|".join(parts))

    def tokenize(self, text: str) -> Generator[Token, None, None]:
        if not text:
            return
        scanner = self.regex.scanner(text)  # type: ignore[attr-defined]
        m: Optional[Match] = None
        for m in iter(scanner.match, None):
            # The following two assertions are to help mypy
            msg = (
                "unexpected value encountered during parsing. Please submit a bug report "
                "at https://github.com/spack/spack/issues/new/choose"
            )
            assert m is not None, msg
            assert m.lastgroup is not None, msg

            token = Token(self.tokens.__members__[m.lastgroup], m.group(), m.start(), m.end())

            # add any subvalues to the token
            subvalues = self.token_subvalues.get(m.lastgroup)
            if subvalues:
                token.subvalues = {name: m.group(name) for name in subvalues}

            yield token
