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

    def __init__(self, kind: TokenBase, value: str, start: int = 0, end: int = 0, **kwargs):
        self.kind = kind
        self.value = value
        self.start = start
        self.end = end
        self.subvalues = kwargs if kwargs else None

    def __repr__(self):
        return str(self)

    def __str__(self):
        parts = [self.kind, self.value]
        if self.subvalues:
            parts += [self.subvalues]
        return f"({', '.join(f'`{p}`' for p in parts)})"

    def __eq__(self, other):
        return (
            self.kind == other.kind
            and self.value == other.value
            and self.subvalues == other.subvalues
        )


def token_match_regex(token: TokenBase):
    """Generate a regular expression that matches the provided token and its subvalues.

    This will extract named capture groups from the provided regex and prefix them with
    token name, so they can coexist together in a larger, joined regular expression.

    Returns:
        A regex with a capture group for the token and rewritten capture groups for any subvalues.

    """
    pairs = []

    def replace(m):
        subvalue_name = m.group(1)
        token_prefixed_subvalue_name = f"{token.name}_{subvalue_name}"
        pairs.append((subvalue_name, token_prefixed_subvalue_name))
        return f"(?P<{token_prefixed_subvalue_name}>"

    # rewrite all subvalue capture groups so they're prefixed with the token name
    rewritten_token_regex = re.sub(r"\(\?P<([^>]+)>", replace, token.regex)

    # construct a regex that matches the token as a whole *and* the subvalue capture groups
    token_regex = f"(?P<{token}>{rewritten_token_regex})"
    return token_regex, pairs


class Tokenizer:
    def __init__(self, tokens: Type[TokenBase]):
        self.tokens = tokens

        # tokens can have named subexpressions, if their regexes define named capture groups.
        # record this so we can associate them with the token
        self.token_subvalues = {}

        parts = []
        for token in tokens:
            token_regex, pairs = token_match_regex(token)
            parts.append(token_regex)
            if pairs:
                self.token_subvalues[token.name] = pairs

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
                if any(m.group(rewritten) for subval, rewritten in subvalues):
                    token.subvalues = {
                        subval: m.group(rewritten) for subval, rewritten in subvalues
                    }

            yield token
