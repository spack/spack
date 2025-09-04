# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import json
import re
import sys

from spack.tokenize import TokenBase

#: Valid name for specs and variants. Here we are not using
#: the previous ``w[\w.-]*`` since that would match most
#: characters that can be part of a word in any language
IDENTIFIER = r"(?:[a-zA-Z_0-9][a-zA-Z_0-9\-]*)"
DOTTED_IDENTIFIER = rf"(?:{IDENTIFIER}(?:\.{IDENTIFIER})+)"
GIT_HASH = r"(?:[A-Fa-f0-9]{40})"
#: Git refs include branch names, and can contain ``.`` and ``/``
GIT_REF = r"(?:[a-zA-Z_0-9][a-zA-Z_0-9./\-]*)"
GIT_VERSION_PATTERN = rf"(?:(?:git\.(?:{GIT_REF}))|(?:{GIT_HASH}))"

#: Substitute a package for a virtual, e.g., c,cxx=gcc.
#: NOTE: Overlaps w/KVP; this should be first if matched in sequence.
VIRTUAL_ASSIGNMENT = (
    r"(?:"
    rf"(?P<virtuals>{IDENTIFIER}(?:,{IDENTIFIER})*)"  # comma-separated virtuals
    rf"=(?P<substitute>{DOTTED_IDENTIFIER}|{IDENTIFIER})"  # package to substitute
    r")"
)

STAR = r"\*"

NAME = r"[a-zA-Z_0-9][a-zA-Z_0-9\-.]*"

HASH = r"[a-zA-Z_0-9]+"

#: These are legal values that *can* be parsed bare, without quotes on the command line.
VALUE = r"(?:[a-zA-Z_0-9\-+\*.,:=%^\~\/\\]+)"

#: Quoted values can be *anything* in between quotes, including escaped quotes.
QUOTED_VALUE = r"(?:'(?:[^']|(?<=\\)')*'|\"(?:[^\"]|(?<=\\)\")*\")"

VERSION = r"=?(?:[a-zA-Z0-9_][a-zA-Z_0-9\-\.]*\b)"
VERSION_RANGE = rf"(?:(?:{VERSION})?:(?:{VERSION}(?!\s*=))?)"
VERSION_LIST = rf"(?:{VERSION_RANGE}|{VERSION})(?:\s*,\s*(?:{VERSION_RANGE}|{VERSION}))*"

#: A filename starts either with a ``.`` or a ``/`` or a ``{name}/``, or on Windows, a drive letter
#: followed by a colon and ``\`` or ``.`` or ``{name}\``
WINDOWS_FILENAME = r"(?:\.|[a-zA-Z0-9-_]*\\|[a-zA-Z]:\\)(?:[a-zA-Z0-9-_\.\\]*)(?:\.json|\.yaml)"
UNIX_FILENAME = r"(?:\.|\/|[a-zA-Z0-9-_]*\/)(?:[a-zA-Z0-9-_\.\/]*)(?:\.json|\.yaml)"
FILENAME = WINDOWS_FILENAME if sys.platform == "win32" else UNIX_FILENAME

#: Values that match this (e.g., variants, flags) can be left unquoted in Spack output
NO_QUOTES_NEEDED = re.compile(r"^[a-zA-Z0-9,/_.\-\[\]]+$")

#: Regex to strip quotes. Group 2 will be the unquoted string.
STRIP_QUOTES = re.compile(r"^(['\"])(.*)\1$")

SPLIT_KVP = re.compile(rf"^({NAME})(:?==?)(.*)$")


class SpecTokens(TokenBase):
    """Enumeration of the different token kinds of tokens in the spec grammar.

    Order of declaration is extremely important, since text containing specs is parsed with a
    single regex obtained by ``"|".join(...)`` of all the regex in the order of declaration.
    """

    # Dependency, with optional virtual assignment specifier
    START_EDGE_PROPERTIES = r"(?:[\^%]\[)"
    END_EDGE_PROPERTIES = rf"(?:\](?:\s*{VIRTUAL_ASSIGNMENT})?)"
    DEPENDENCY = rf"(?:[\^\%](?:\s*{VIRTUAL_ASSIGNMENT})?)"

    # Version
    VERSION_HASH_PAIR = rf"(?:@(?:{GIT_VERSION_PATTERN})=(?:{VERSION}))"
    GIT_VERSION = rf"@(?:{GIT_VERSION_PATTERN})"
    VERSION = rf"(?:@\s*(?:{VERSION_LIST}))"

    # Variants
    PROPAGATED_BOOL_VARIANT = rf"(?:(?:\+\+|~~|--)\s*{NAME})"
    BOOL_VARIANT = rf"(?:[~+-]\s*{NAME})"
    PROPAGATED_KEY_VALUE_PAIR = rf"(?:{NAME}:?==(?:{VALUE}|{QUOTED_VALUE}))"
    KEY_VALUE_PAIR = rf"(?:{NAME}:?=(?:{VALUE}|{QUOTED_VALUE}))"

    # FILENAME
    FILENAME = rf"(?:{FILENAME})"

    # Package name
    FULLY_QUALIFIED_PACKAGE_NAME = rf"(?:{DOTTED_IDENTIFIER})"
    UNQUALIFIED_PACKAGE_NAME = rf"(?:{IDENTIFIER}|{STAR})"

    # DAG hash
    DAG_HASH = rf"(?:/(?:{HASH}))"

    # White spaces
    WS = r"(?:\s+)"

    # Unexpected character(s)
    UNEXPECTED = r"(?:.[\s]*)"


def quote_if_needed(value: str) -> str:
    """Add quotes around the value if it requires quotes.

    This will add quotes around the value unless it matches :data:`NO_QUOTES_NEEDED`.

    This adds:

    * single quotes by default
    * double quotes around any value that contains single quotes

    If double quotes are used, we json-escape the string. That is, we escape ``\\``,
    ``"``, and control codes.

    """
    if NO_QUOTES_NEEDED.match(value):
        return value

    return json.dumps(value) if "'" in value else f"'{value}'"


def strip_quotes_and_unescape(string: str) -> str:
    """Remove surrounding single or double quotes from string, if present."""
    match = STRIP_QUOTES.match(string)
    if not match:
        return string

    # replace any escaped quotes with bare quotes
    quote, result = match.groups()
    return result.replace(rf"\{quote}", quote)


def quote_kvp(string: str) -> str:
    """For strings like ``name=value`` or ``name==value``, quote and escape the value if needed.

    This is a compromise to respect quoting of key-value pairs on the CLI. The shell
    strips quotes from quoted arguments, so we cannot know *exactly* how CLI arguments
    were quoted. To compensate, we re-add quotes around anything staritng with ``name=``
    or ``name==``, and we assume the rest of the argument is the value. This covers the
    common cases of passign flags, e.g., ``cflags="-O2 -g"`` on the command line.
    """
    match = SPLIT_KVP.match(string)
    if not match:
        return string

    key, delim, value = match.groups()
    return f"{key}{delim}{quote_if_needed(value)}"
