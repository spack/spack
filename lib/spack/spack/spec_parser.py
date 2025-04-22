# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
"""Parser for spec literals

Here is the EBNF grammar for a spec::

    spec          = [name] [node_options] { ^[edge_properties] node } |
                    [name] [node_options] hash |
                    filename

    node          =  name [node_options] |
                     [name] [node_options] hash |
                     filename

    node_options    = [@(version_list|version_pair)] [%compiler] { variant }
    edge_properties = [ { bool_variant | key_value } ]

    hash          = / id
    filename      = (.|/|[a-zA-Z0-9-_]*/)([a-zA-Z0-9-_./]*)(.json|.yaml)

    name          = id | namespace id
    namespace     = { id . }

    variant       = bool_variant | key_value | propagated_bv | propagated_kv
    bool_variant  =  +id |  ~id |  -id
    propagated_bv = ++id | ~~id | --id
    key_value     =  id=id |  id=quoted_id
    propagated_kv = id==id | id==quoted_id

    compiler      = id [@version_list]

    version_pair  = git_version=vid
    version_list  = (version|version_range) [ { , (version|version_range)} ]
    version_range = vid:vid | vid: | :vid | :
    version       = vid

    git_version   = git.(vid) | git_hash
    git_hash      = [A-Fa-f0-9]{40}

    quoted_id     = " id_with_ws " | ' id_with_ws '
    id_with_ws    = [a-zA-Z0-9_][a-zA-Z_0-9-.\\s]*
    vid           = [a-zA-Z0-9_][a-zA-Z_0-9-.]*
    id            = [a-zA-Z0-9_][a-zA-Z_0-9-]*

Identifiers using the <name>=<value> command, such as architectures and
compiler flags, require a space before the name.

There is one context-sensitive part: ids in versions may contain '.', while
other ids may not.

There is one ambiguity: since '-' is allowed in an id, you need to put
whitespace space before -variant for it to be tokenized properly.  You can
either use whitespace, or you can just use ~variant since it means the same
thing.  Spack uses ~variant in directory names and in the canonical form of
specs to avoid ambiguity.  Both are provided because ~ can cause shell
expansion when it is the first character in an id typed on the command line.
"""
import json
import pathlib
import re
import sys
import traceback
import warnings
from typing import Iterator, List, Optional, Tuple, Union

from llnl.util.tty import color

import spack.deptypes
import spack.error
import spack.paths
import spack.spec
import spack.util.spack_yaml
import spack.version
from spack.aliases import LEGACY_COMPILER_TO_BUILTIN
from spack.tokenize import Token, TokenBase, Tokenizer

#: Valid name for specs and variants. Here we are not using
#: the previous "w[\w.-]*" since that would match most
#: characters that can be part of a word in any language
IDENTIFIER = r"(?:[a-zA-Z_0-9][a-zA-Z_0-9\-]*)"
DOTTED_IDENTIFIER = rf"(?:{IDENTIFIER}(?:\.{IDENTIFIER})+)"
GIT_HASH = r"(?:[A-Fa-f0-9]{40})"
#: Git refs include branch names, and can contain "." and "/"
GIT_REF = r"(?:[a-zA-Z_0-9][a-zA-Z_0-9./\-]*)"
GIT_VERSION_PATTERN = rf"(?:(?:git\.(?:{GIT_REF}))|(?:{GIT_HASH}))"

NAME = r"[a-zA-Z_0-9][a-zA-Z_0-9\-.]*"

HASH = r"[a-zA-Z_0-9]+"

#: These are legal values that *can* be parsed bare, without quotes on the command line.
VALUE = r"(?:[a-zA-Z_0-9\-+\*.,:=\~\/\\]+)"

#: Quoted values can be *anything* in between quotes, including escaped quotes.
QUOTED_VALUE = r"(?:'(?:[^']|(?<=\\)')*'|\"(?:[^\"]|(?<=\\)\")*\")"

VERSION = r"=?(?:[a-zA-Z0-9_][a-zA-Z_0-9\-\.]*\b)"
VERSION_RANGE = rf"(?:(?:{VERSION})?:(?:{VERSION}(?!\s*=))?)"
VERSION_LIST = rf"(?:{VERSION_RANGE}|{VERSION})(?:\s*,\s*(?:{VERSION_RANGE}|{VERSION}))*"

SPLIT_KVP = re.compile(rf"^({NAME})(:?==?)(.*)$")

#: Regex with groups to use for splitting %[virtuals=...] tokens
SPLIT_COMPILER_TOKEN = re.compile(rf"^%\[virtuals=({VALUE}|{QUOTED_VALUE})]\s*(.*)$")

#: A filename starts either with a "." or a "/" or a "{name}/, or on Windows, a drive letter
#: followed by a colon and "\" or "." or {name}\
WINDOWS_FILENAME = r"(?:\.|[a-zA-Z0-9-_]*\\|[a-zA-Z]:\\)(?:[a-zA-Z0-9-_\.\\]*)(?:\.json|\.yaml)"
UNIX_FILENAME = r"(?:\.|\/|[a-zA-Z0-9-_]*\/)(?:[a-zA-Z0-9-_\.\/]*)(?:\.json|\.yaml)"
FILENAME = WINDOWS_FILENAME if sys.platform == "win32" else UNIX_FILENAME

#: Regex to strip quotes. Group 2 will be the unquoted string.
STRIP_QUOTES = re.compile(r"^(['\"])(.*)\1$")

#: Values that match this (e.g., variants, flags) can be left unquoted in Spack output
NO_QUOTES_NEEDED = re.compile(r"^[a-zA-Z0-9,/_.-]+$")


class SpecTokens(TokenBase):
    """Enumeration of the different token kinds in the spec grammar.
    Order of declaration is extremely important, since text containing specs is parsed with a
    single regex obtained by ``"|".join(...)`` of all the regex in the order of declaration.
    """

    # Dependency
    START_EDGE_PROPERTIES = r"(?:\^\[)"
    END_EDGE_PROPERTIES = r"(?:\])"
    DEPENDENCY = r"(?:\^)"
    # Version
    VERSION_HASH_PAIR = rf"(?:@(?:{GIT_VERSION_PATTERN})=(?:{VERSION}))"
    GIT_VERSION = rf"@(?:{GIT_VERSION_PATTERN})"
    VERSION = rf"(?:@\s*(?:{VERSION_LIST}))"
    # Variants
    PROPAGATED_BOOL_VARIANT = rf"(?:(?:\+\+|~~|--)\s*{NAME})"
    BOOL_VARIANT = rf"(?:[~+-]\s*{NAME})"
    PROPAGATED_KEY_VALUE_PAIR = rf"(?:{NAME}:?==(?:{VALUE}|{QUOTED_VALUE}))"
    KEY_VALUE_PAIR = rf"(?:{NAME}:?=(?:{VALUE}|{QUOTED_VALUE}))"
    # Compilers
    COMPILER_AND_VERSION = rf"(?:%\s*(?:{NAME})(?:[\s]*)@\s*(?:{VERSION_LIST}))"
    COMPILER = rf"(?:%\s*(?:{NAME}))"
    COMPILER_AND_VERSION_WITH_VIRTUALS = (
        rf"(?:%\[virtuals=(?:{VALUE}|{QUOTED_VALUE})\]"
        rf"\s*(?:{NAME})(?:[\s]*)@\s*(?:{VERSION_LIST}))"
    )
    COMPILER_WITH_VIRTUALS = rf"(?:%\[virtuals=(?:{VALUE}|{QUOTED_VALUE})\]\s*(?:{NAME}))"
    # FILENAME
    FILENAME = rf"(?:{FILENAME})"
    # Package name
    FULLY_QUALIFIED_PACKAGE_NAME = rf"(?:{DOTTED_IDENTIFIER})"
    UNQUALIFIED_PACKAGE_NAME = rf"(?:{IDENTIFIER})"
    # DAG hash
    DAG_HASH = rf"(?:/(?:{HASH}))"
    # White spaces
    WS = r"(?:\s+)"
    # Unexpected character(s)
    UNEXPECTED = r"(?:.[\s]*)"


#: Tokenizer that includes all the regexes in the SpecTokens enum
SPEC_TOKENIZER = Tokenizer(SpecTokens)


def tokenize(text: str) -> Iterator[Token]:
    """Return a token generator from the text passed as input.

    Raises:
        SpecTokenizationError: when unexpected characters are found in the text
    """
    for token in SPEC_TOKENIZER.tokenize(text):
        if token.kind == SpecTokens.UNEXPECTED:
            raise SpecTokenizationError(list(SPEC_TOKENIZER.tokenize(text)), text)
        yield token


class TokenContext:
    """Token context passed around by parsers"""

    __slots__ = "token_stream", "current_token", "next_token"

    def __init__(self, token_stream: Iterator[Token]):
        self.token_stream = token_stream
        self.current_token = None
        self.next_token = None
        self.advance()

    def advance(self):
        """Advance one token"""
        self.current_token, self.next_token = self.next_token, next(self.token_stream, None)

    def accept(self, kind: SpecTokens):
        """If the next token is of the specified kind, advance the stream and return True.
        Otherwise return False.
        """
        if self.next_token and self.next_token.kind == kind:
            self.advance()
            return True
        return False

    def expect(self, *kinds: SpecTokens):
        return self.next_token and self.next_token.kind in kinds


class SpecTokenizationError(spack.error.SpecSyntaxError):
    """Syntax error in a spec string"""

    def __init__(self, tokens: List[Token], text: str):
        message = f"unexpected characters in the spec string\n{text}\n"

        underline = ""
        for token in tokens:
            is_error = token.kind == SpecTokens.UNEXPECTED
            underline += ("^" if is_error else " ") * (token.end - token.start)

        message += color.colorize(f"@*r{{{underline}}}")
        super().__init__(message)


def _warn_about_variant_after_compiler(literal_str: str, issues: List[str]):
    """Issue a warning if variant or other token is preceded by a compiler token. The warning is
    only issued if it's actionable: either we know the config file it originates from, or we have
    call site that's not internal to Spack."""
    ignore = [spack.paths.lib_path, spack.paths.bin_path]
    mark = spack.util.spack_yaml.get_mark_from_yaml_data(literal_str)
    issue_str = ", ".join(issues)
    error = f"{issue_str} in `{literal_str}`"

    # warning from config file
    if mark:
        warnings.warn(f"{mark.name}:{mark.line + 1}: {error}")
        return

    # warning from hopefully package.py
    for frame in reversed(traceback.extract_stack()):
        if frame.lineno and not any(frame.filename.startswith(path) for path in ignore):
            warnings.warn_explicit(
                error,
                category=spack.error.SpackAPIWarning,
                filename=frame.filename,
                lineno=frame.lineno,
            )
            return


class SpecParser:
    """Parse text into specs"""

    __slots__ = "literal_str", "ctx"

    def __init__(self, literal_str: str):
        self.literal_str = literal_str
        self.ctx = TokenContext(filter(lambda x: x.kind != SpecTokens.WS, tokenize(literal_str)))

    def tokens(self) -> List[Token]:
        """Return the entire list of token from the initial text. White spaces are
        filtered out.
        """
        return list(filter(lambda x: x.kind != SpecTokens.WS, tokenize(self.literal_str)))

    def next_spec(
        self, initial_spec: Optional["spack.spec.Spec"] = None
    ) -> Optional["spack.spec.Spec"]:
        """Return the next spec parsed from text.

        Args:
            initial_spec: object where to parse the spec. If None a new one
                will be created.

        Return
            The spec that was parsed
        """
        if not self.ctx.next_token:
            return initial_spec

        def add_dependency(dep, **edge_properties):
            """wrapper around root_spec._add_dependency"""
            try:
                root_spec._add_dependency(dep, **edge_properties)
            except spack.error.SpecError as e:
                raise SpecParsingError(str(e), self.ctx.current_token, self.literal_str) from e

        initial_spec = initial_spec or spack.spec.Spec()
        root_spec, parser_warnings = SpecNodeParser(self.ctx, self.literal_str).parse(initial_spec)
        while True:
            if self.ctx.accept(SpecTokens.START_EDGE_PROPERTIES):
                edge_properties = EdgeAttributeParser(self.ctx, self.literal_str).parse()
                edge_properties.setdefault("depflag", 0)
                edge_properties.setdefault("virtuals", ())
                dependency, warnings = self._parse_node(root_spec)
                parser_warnings.extend(warnings)
                add_dependency(dependency, **edge_properties)

            elif self.ctx.accept(SpecTokens.DEPENDENCY):
                dependency, warnings = self._parse_node(root_spec)
                parser_warnings.extend(warnings)
                add_dependency(dependency, depflag=0, virtuals=())

            else:
                break

        if parser_warnings:
            _warn_about_variant_after_compiler(self.literal_str, parser_warnings)

        return root_spec

    def _parse_node(self, root_spec):
        dependency, parser_warnings = SpecNodeParser(self.ctx, self.literal_str).parse()
        if dependency is None:
            msg = (
                "the dependency sigil and any optional edge attributes must be followed by a "
                "package name or a node attribute (version, variant, etc.)"
            )
            raise SpecParsingError(msg, self.ctx.current_token, self.literal_str)
        if root_spec.concrete:
            raise spack.spec.RedundantSpecError(root_spec, "^" + str(dependency))
        return dependency, parser_warnings

    def all_specs(self) -> List["spack.spec.Spec"]:
        """Return all the specs that remain to be parsed"""
        return list(iter(self.next_spec, None))


class SpecNodeParser:
    """Parse a single spec node from a stream of tokens"""

    __slots__ = "ctx", "has_version", "literal_str"

    def __init__(self, ctx, literal_str):
        self.ctx = ctx
        self.literal_str = literal_str
        self.has_version = False

    def parse(
        self, initial_spec: Optional["spack.spec.Spec"] = None
    ) -> Tuple["spack.spec.Spec", List[str]]:
        """Parse a single spec node from a stream of tokens

        Args:
            initial_spec: object to be constructed

        Return
            The object passed as argument
        """
        parser_warnings: List[str] = []
        last_compiler = None

        if initial_spec is None:
            initial_spec = spack.spec.Spec()

        if not self.ctx.next_token or self.ctx.expect(SpecTokens.DEPENDENCY):
            return initial_spec, parser_warnings

        # If we start with a package name we have a named spec, we cannot
        # accept another package name afterwards in a node
        if self.ctx.accept(SpecTokens.UNQUALIFIED_PACKAGE_NAME):
            initial_spec.name = self.ctx.current_token.value

        elif self.ctx.accept(SpecTokens.FULLY_QUALIFIED_PACKAGE_NAME):
            parts = self.ctx.current_token.value.split(".")
            name = parts[-1]
            namespace = ".".join(parts[:-1])
            initial_spec.name = name
            initial_spec.namespace = namespace

        elif self.ctx.accept(SpecTokens.FILENAME):
            return FileParser(self.ctx).parse(initial_spec), parser_warnings

        def raise_parsing_error(string: str, cause: Optional[Exception] = None):
            """Raise a spec parsing error with token context."""
            raise SpecParsingError(string, self.ctx.current_token, self.literal_str) from cause

        def add_flag(name: str, value: Union[str, bool], propagate: bool, concrete: bool):
            """Wrapper around ``Spec._add_flag()`` that adds parser context to errors raised."""
            try:
                initial_spec._add_flag(name, value, propagate, concrete)
            except Exception as e:
                raise_parsing_error(str(e), e)

        def warn_if_after_compiler(token: str):
            """Register a warning for %compiler followed by +variant that will in the future apply
            to the compiler instead of the current root."""
            if last_compiler:
                parser_warnings.append(f"`{token}` should go before `{last_compiler}`")

        while True:
            if (
                self.ctx.accept(SpecTokens.COMPILER)
                or self.ctx.accept(SpecTokens.COMPILER_AND_VERSION)
                or self.ctx.accept(SpecTokens.COMPILER_WITH_VIRTUALS)
                or self.ctx.accept(SpecTokens.COMPILER_AND_VERSION_WITH_VIRTUALS)
            ):
                current_token = self.ctx.current_token
                if current_token.kind in (
                    SpecTokens.COMPILER_WITH_VIRTUALS,
                    SpecTokens.COMPILER_AND_VERSION_WITH_VIRTUALS,
                ):
                    m = SPLIT_COMPILER_TOKEN.match(current_token.value)
                    assert m, "SPLIT_COMPILER_TOKEN and COMPILER_* do not agree."
                    virtuals_str, compiler_str = m.groups()
                    virtuals = tuple(virtuals_str.strip("'\" ").split(","))
                else:
                    virtuals = tuple()
                    compiler_str = current_token.value[1:]

                build_dependency = spack.spec.Spec(compiler_str)
                if build_dependency.name in LEGACY_COMPILER_TO_BUILTIN:
                    build_dependency.name = LEGACY_COMPILER_TO_BUILTIN[build_dependency.name]

                initial_spec._add_dependency(
                    build_dependency, depflag=spack.deptypes.BUILD, virtuals=virtuals, direct=True
                )
                last_compiler = self.ctx.current_token.value

            elif (
                self.ctx.accept(SpecTokens.VERSION_HASH_PAIR)
                or self.ctx.accept(SpecTokens.GIT_VERSION)
                or self.ctx.accept(SpecTokens.VERSION)
            ):
                if self.has_version:
                    raise_parsing_error("Spec cannot have multiple versions")

                initial_spec.versions = spack.version.VersionList(
                    [spack.version.from_string(self.ctx.current_token.value[1:])]
                )
                initial_spec.attach_git_version_lookup()
                self.has_version = True
                warn_if_after_compiler(self.ctx.current_token.value)

            elif self.ctx.accept(SpecTokens.BOOL_VARIANT):
                name = self.ctx.current_token.value[1:].strip()
                variant_value = self.ctx.current_token.value[0] == "+"
                add_flag(name, variant_value, propagate=False, concrete=True)
                warn_if_after_compiler(self.ctx.current_token.value)

            elif self.ctx.accept(SpecTokens.PROPAGATED_BOOL_VARIANT):
                name = self.ctx.current_token.value[2:].strip()
                variant_value = self.ctx.current_token.value[0:2] == "++"
                add_flag(name, variant_value, propagate=True, concrete=True)
                warn_if_after_compiler(self.ctx.current_token.value)

            elif self.ctx.accept(SpecTokens.KEY_VALUE_PAIR):
                name, value = self.ctx.current_token.value.split("=", maxsplit=1)
                concrete = name.endswith(":")
                if concrete:
                    name = name[:-1]

                add_flag(
                    name, strip_quotes_and_unescape(value), propagate=False, concrete=concrete
                )
                warn_if_after_compiler(self.ctx.current_token.value)

            elif self.ctx.accept(SpecTokens.PROPAGATED_KEY_VALUE_PAIR):
                name, value = self.ctx.current_token.value.split("==", maxsplit=1)
                concrete = name.endswith(":")
                if concrete:
                    name = name[:-1]
                add_flag(name, strip_quotes_and_unescape(value), propagate=True, concrete=concrete)
                warn_if_after_compiler(self.ctx.current_token.value)

            elif self.ctx.expect(SpecTokens.DAG_HASH):
                if initial_spec.abstract_hash:
                    break
                self.ctx.accept(SpecTokens.DAG_HASH)
                initial_spec.abstract_hash = self.ctx.current_token.value[1:]
                warn_if_after_compiler(self.ctx.current_token.value)

            else:
                break

        return initial_spec, parser_warnings


class FileParser:
    """Parse a single spec from a JSON or YAML file"""

    __slots__ = ("ctx",)

    def __init__(self, ctx):
        self.ctx = ctx

    def parse(self, initial_spec: "spack.spec.Spec") -> "spack.spec.Spec":
        """Parse a spec tree from a specfile.

        Args:
            initial_spec: object where to parse the spec

        Return
            The initial_spec passed as argument, once constructed
        """
        file = pathlib.Path(self.ctx.current_token.value)

        if not file.exists():
            raise spack.spec.NoSuchSpecFileError(f"No such spec file: '{file}'")

        with file.open("r", encoding="utf-8") as stream:
            if str(file).endswith(".json"):
                spec_from_file = spack.spec.Spec.from_json(stream)
            else:
                spec_from_file = spack.spec.Spec.from_yaml(stream)
        initial_spec._dup(spec_from_file)
        return initial_spec


class EdgeAttributeParser:
    __slots__ = "ctx", "literal_str"

    def __init__(self, ctx, literal_str):
        self.ctx = ctx
        self.literal_str = literal_str

    def parse(self):
        attributes = {}
        while True:
            if self.ctx.accept(SpecTokens.KEY_VALUE_PAIR):
                name, value = self.ctx.current_token.value.split("=", maxsplit=1)
                if name.endswith(":"):
                    name = name[:-1]
                value = value.strip("'\" ").split(",")
                attributes[name] = value
                if name not in ("deptypes", "virtuals"):
                    msg = (
                        "the only edge attributes that are currently accepted "
                        'are "deptypes" and "virtuals"'
                    )
                    raise SpecParsingError(msg, self.ctx.current_token, self.literal_str)
            # TODO: Add code to accept bool variants here as soon as use variants are implemented
            elif self.ctx.accept(SpecTokens.END_EDGE_PROPERTIES):
                break
            else:
                msg = "unexpected token in edge attributes"
                raise SpecParsingError(msg, self.ctx.next_token, self.literal_str)

        # Turn deptypes=... to depflag representation
        if "deptypes" in attributes:
            deptype_string = attributes.pop("deptypes")
            attributes["depflag"] = spack.deptypes.canonicalize(deptype_string)
        return attributes


def parse(text: str) -> List["spack.spec.Spec"]:
    """Parse text into a list of strings

    Args:
        text (str): text to be parsed

    Return:
        List of specs
    """
    return SpecParser(text).all_specs()


def parse_one_or_raise(
    text: str, initial_spec: Optional["spack.spec.Spec"] = None
) -> "spack.spec.Spec":
    """Parse exactly one spec from text and return it, or raise

    Args:
        text (str): text to be parsed
        initial_spec: buffer where to parse the spec. If None a new one will be created.
    """
    parser = SpecParser(text)
    result = parser.next_spec(initial_spec)
    next_token = parser.ctx.next_token

    if next_token:
        message = f"expected a single spec, but got more:\n{text}"
        underline = f"\n{' ' * next_token.start}{'^' * len(next_token.value)}"
        message += color.colorize(f"@*r{{{underline}}}")
        raise ValueError(message)

    if result is None:
        raise ValueError("expected a single spec, but got none")

    return result


class SpecParsingError(spack.error.SpecSyntaxError):
    """Error when parsing tokens"""

    def __init__(self, message, token, text):
        message += f"\n{text}"
        underline = f"\n{' '*token.start}{'^'*(token.end - token.start)}"
        message += color.colorize(f"@*r{{{underline}}}")
        super().__init__(message)


def strip_quotes_and_unescape(string: str) -> str:
    """Remove surrounding single or double quotes from string, if present."""
    match = STRIP_QUOTES.match(string)
    if not match:
        return string

    # replace any escaped quotes with bare quotes
    quote, result = match.groups()
    return result.replace(rf"\{quote}", quote)


def quote_if_needed(value: str) -> str:
    """Add quotes around the value if it requires quotes.

    This will add quotes around the value unless it matches ``NO_QUOTES_NEEDED``.

    This adds:
    * single quotes by default
    * double quotes around any value that contains single quotes

    If double quotes are used, we json-escape the string. That is, we escape ``\\``,
    ``"``, and control codes.

    """
    if NO_QUOTES_NEEDED.match(value):
        return value

    return json.dumps(value) if "'" in value else f"'{value}'"
