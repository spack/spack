# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
"""This module provides building blocks for tokenizing strings. Users can define tokens by
inheriting from TokenBase and defining tokens as ordered enum members. The Tokenizer class can then
be used to iterate over tokens in a string."""

import enum
import re
from typing import Dict, Generator, Match, Optional, Type


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
    """Tokenizer for the tokens of a :class:`TokenBase` enum.

    The regexes of the tokens are joined into a single regex, in order of declaration, with a
    named group per token. Tokens are matched by scanning the input with this regex: the kind
    of a token is the name of the outermost group that matched, ``match.lastgroup``.
    """

    def __init__(self, tokens: Type[TokenBase], *, skip_whitespace: bool = False):
        """
        Args:
            tokens: enum of tokens
            skip_whitespace: if True, whitespace before a token is consumed by the regex itself
                and is not part of the token, so no whitespace token is needed
        """
        self.tokens = tokens
        #: Token kind by name of the group that matched it
        self.kinds: Dict[str, TokenBase] = {t.name: t for t in tokens}
        alternation = "|".join(f"(?P<{t.name}>{t.regex})" for t in tokens)
        self.regex = re.compile(rf"\s*(?:{alternation})" if skip_whitespace else alternation)

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

            # Take the value and span from the group of the token, not the whole match, which
            # may include skipped whitespace
            name = m.lastgroup
            yield Token(self.kinds[name], m.group(name), m.start(name), m.end(name))
