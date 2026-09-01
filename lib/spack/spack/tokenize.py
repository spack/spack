# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
"""This module provides building blocks for tokenizing strings. Users can define tokens by
inheriting from TokenBase and defining tokens as ordered enum members. The Tokenizer class can then
be used to iterate over tokens in a string."""

import enum
import re
from typing import Generator, Match, Optional, Sequence, Type


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

    __slots__ = "kind", "value", "start", "end"

    def __init__(self, kind: TokenBase, value: str, start: int = 0, end: int = 0):
        self.kind = kind
        self.value = value
        self.start = start
        self.end = end

    def __repr__(self):
        return str(self)

    def __str__(self):
        return f"(`{self.kind}`, `{self.value}`)"

    def __eq__(self, other):
        return self.kind == other.kind and self.value == other.value


class Tokenizer:
    """Tokenizer for a token enum.

    The tokens are matched as a single regex, in order of declaration, unless ``first`` lists
    kinds that should be tried before the others.
    """

    def __init__(self, tokens: Type[TokenBase], first: Sequence[TokenBase] = ()):
        self.tokens = tokens
        ordered = list(first) + [t for t in tokens if t not in first]
        self.regex = re.compile("|".join(f"(?P<{t.name}>{t.regex})" for t in ordered))

    def _token(self, m: Match) -> Token:
        msg = (
            "unexpected value encountered during parsing. Please submit a bug report "
            "at https://github.com/spack/spack/issues/new/choose"
        )
        assert m.lastgroup is not None, msg
        return Token(self.tokens.__members__[m.lastgroup], m.group(), m.start(), m.end())

    def match(self, text: str, pos: int = 0) -> Optional[Token]:
        """Return the token that matches at position ``pos`` of ``text``, if any."""
        m = self.regex.match(text, pos)
        return self._token(m) if m else None

    def tokenize(self, text: str) -> Generator[Token, None, None]:
        if not text:
            return

        scanner = self.regex.scanner(text)  # type: ignore[attr-defined]
        for m in iter(scanner.match, None):
            yield self._token(m)
