# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
"""Parser for dotenv (``.env``) files.

The supported grammar follows the common dotenv conventions (as implemented by
``python-dotenv``)::

    # Full line comment
    KEY=value                  # unquoted, trailing comment and whitespace stripped
    export KEY=value           # optional ``export`` prefix is ignored
    KEY = value                # whitespace around ``=`` is allowed
    KEY='literal ${NOT_EXPANDED}'
    KEY="escapes\\n and ${EXPANDED} variables"
    KEY="values in double or
    single quotes may span lines"
    KEY=                       # empty string
    KEY                        # no ``=``: key is defined without a value (None)

Lines that do not conform to the grammar are skipped. A quoted value that is never
closed is skipped along with only the line it starts on.

Variable expansion (``${VAR}``, ``${VAR:-default}`` and ``${VAR-default}``) applies to
unquoted and double quoted values. Variables are resolved against keys defined earlier
in the file first, then the process environment. ``${VAR:-default}`` uses the default
when ``VAR`` is unset or empty, ``${VAR-default}`` only when ``VAR`` is unset.
"""

import os
import re
from pathlib import Path
from typing import Dict, Optional, Union

EnvDict = Dict[str, Optional[str]]

_WHITESPACE = re.compile(r"[ \t]*")
_EXPORT = re.compile(r"export[ \t]+")
_KEY = re.compile(r"[A-Za-z_][A-Za-z0-9_.\-]*")
_UNQUOTED_VALUE = re.compile(r"[^\r\n]*")
_INLINE_COMMENT = re.compile(r"\s+#.*$|^#.*$")
_REST_OF_LINE = re.compile(r"[^\n]*")
_EXPANSION = re.compile(
    r"\$\{(?P<name>[A-Za-z_][A-Za-z0-9_]*)(?:(?P<op>:?-)(?P<default>[^}]*))?\}"
)

_DOUBLE_QUOTE_ESCAPES = {
    "\\": "\\",
    '"': '"',
    "'": "'",
    "$": "$",
    "a": "\a",
    "b": "\b",
    "f": "\f",
    "n": "\n",
    "r": "\r",
    "t": "\t",
    "v": "\v",
}
_SINGLE_QUOTE_ESCAPES = {"\\": "\\", "'": "'"}


class _MalformedLine(Exception):
    """Raised internally when a line does not conform to the grammar"""


class Dotenv:
    """Lazily parsed view of a dotenv file.

    A file that does not exist is treated as empty.
    """

    def __init__(self, path: Union[str, Path], expand: bool = True):
        self._dotenv_file = Path(path)
        self._expand = expand
        self._env: Optional[EnvDict] = None

    def _read_contents(self) -> EnvDict:
        if self._env is not None:
            return self._env

        if not self._dotenv_file.is_file():
            self._env = {}
            return self._env

        with self._dotenv_file.open("r", encoding="utf-8") as f:
            text = f.read()

        self._env = _Parser(text, self._expand).parse()
        return self._env

    @property
    def env(self) -> EnvDict:
        return self._read_contents()

    def load(self, override: bool = False) -> None:
        """Set the variables from the dotenv file in ``os.environ``.

        Keys without a value are skipped. Existing environment variables are only
        replaced when ``override`` is True.
        """
        for key, value in self._read_contents().items():
            if value is None:
                continue
            if override or key not in os.environ:
                os.environ[key] = value


class _Parser:
    def __init__(self, text: str, expand: bool):
        self.text = text
        self.expand = expand
        self.pos = 0
        self.env: EnvDict = {}

    def peek(self) -> str:
        return self.text[self.pos : self.pos + 1]

    def match(self, regex: "re.Pattern") -> Optional["re.Match"]:
        m = regex.match(self.text, self.pos)
        if m:
            self.pos = m.end()
        return m

    def at_end_of_line(self) -> bool:
        return self.pos >= len(self.text) or self.text.startswith(("\n", "\r\n"), self.pos)

    def end_line(self) -> None:
        """Consume optional trailing whitespace and comment, then the line terminator"""
        self.match(_WHITESPACE)
        if self.peek() == "#":
            self.match(_REST_OF_LINE)
        if not self.at_end_of_line():
            raise _MalformedLine()
        if self.peek() == "\r":
            self.pos += 1
        self.pos += 1

    def parse(self) -> EnvDict:
        while self.pos < len(self.text):
            self.match(_WHITESPACE)
            if self.at_end_of_line() or self.peek() == "#":
                self.end_line()
                continue
            start = self.pos
            try:
                self.parse_binding()
            except _MalformedLine:
                self.pos = start
                self.skip_line()
        return self.env

    def skip_line(self) -> None:
        self.match(_REST_OF_LINE)
        self.pos += 1

    def parse_binding(self) -> None:
        start = self.pos
        # "export" is only a prefix if a key follows it, otherwise it is the key itself
        if self.match(_EXPORT) and not _KEY.match(self.text, self.pos):
            self.pos = start

        key = self.match(_KEY)
        if not key:
            raise _MalformedLine()

        self.match(_WHITESPACE)
        if self.peek() != "=":
            # A bare key defines a variable without a value
            self.end_line()
            self.env[key.group()] = None
            return

        self.pos += 1
        self.match(_WHITESPACE)

        quote = self.peek()
        if quote == "'":
            value = self.parse_quoted(quote, _SINGLE_QUOTE_ESCAPES, expand=False)
        elif quote == '"':
            value = self.parse_quoted(quote, _DOUBLE_QUOTE_ESCAPES, expand=self.expand)
        else:
            value = self.parse_unquoted()

        self.end_line()
        self.env[key.group()] = value

    def parse_unquoted(self) -> str:
        raw = self.match(_UNQUOTED_VALUE).group()
        raw = _INLINE_COMMENT.sub("", raw).rstrip()
        return self.substitute(raw, {}, self.expand)

    def parse_quoted(self, quote: str, escapes: Dict[str, str], expand: bool) -> str:
        start = self.pos
        self.pos += 1
        while True:
            end = self.text.find(quote, self.pos)
            if end < 0:
                raise _MalformedLine()
            # The quote is escaped if preceded by an odd number of backslashes
            backslashes = end - len(self.text[:end].rstrip("\\"))
            self.pos = end + 1
            if backslashes % 2 == 0:
                break
        return self.substitute(self.text[start + 1 : end], escapes, expand)

    def substitute(self, raw: str, escapes: Dict[str, str], expand: bool) -> str:
        """Process escape sequences and variable expansions in a single pass, so that
        escaped ``$`` and values of expanded variables are never re-interpreted"""
        result = []
        i = 0
        while i < len(raw):
            c = raw[i]
            if c == "\\" and escapes and i + 1 < len(raw):
                nxt = raw[i + 1]
                # Unknown escape sequences are kept verbatim
                result.append(escapes.get(nxt, c + nxt))
                i += 2
                continue
            m = _EXPANSION.match(raw, i) if expand and c == "$" else None
            if m:
                result.append(self.resolve(m))
                i = m.end()
                continue
            result.append(c)
            i += 1
        return "".join(result)

    def resolve(self, m: "re.Match") -> str:
        name, op, default = m.group("name", "op", "default")
        value = self.env.get(name)
        if value is None:
            value = os.environ.get(name)
        if op == "-" and value is None:
            return default
        if op == ":-" and not value:
            return default
        return value or ""
