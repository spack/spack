# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
"""Parser for spec literals"""
import pathlib
import re
from enum import Enum, auto
from typing import Iterator, List, Optional

import spack.error
import spack.spec
import spack.variant
import spack.version

#: Valid name for specs and variants. Here we are not using
#: the previous "w[\w.-]*" since that would match most
#: characters that can be part of a word in any language
VALID_NAME_WITHOUT_DOTS = r"[a-zA-Z_0-9][a-zA-Z_0-9\-]*"
VALID_NAME_WITH_DOTS = rf"{VALID_NAME_WITHOUT_DOTS}(\.{VALID_NAME_WITHOUT_DOTS})+"
VALID_GIT_VERSION = rf"(((git.)?({VALID_NAME_WITH_DOTS}))|({VALID_NAME_WITHOUT_DOTS}))"

VALID_NAME = r"[a-zA-Z_0-9][a-zA-Z_0-9\-.]*"

VALID_HASH = r"[a-zA-Z_0-9]+"

#: A filename starts either with a "." or a "/" or a "{name}/"
VALID_FILENAME = r"(\.|\/|[a-zA-Z0-9-_]*\/)([a-zA-Z0-9-_\.\/]*)(\.json|\.yaml)"

VALID_VALUE = r"([a-zA-Z_0-9\-+\*.,:=\~\/\\]+)"
VALID_QUOTED_VALUE = r"[\"']+([a-zA-Z_0-9\-+\*.,:=\~\/\\\s]+)[\"']+"

VALID_VERSION = r"([a-zA-Z_0-9-.][a-zA-Z_0-9-.]*)"
VALID_VERSION_RANGE = rf"({VALID_VERSION}:{VALID_VERSION}|:{VALID_VERSION}|{VALID_VERSION}:|:)"
VALID_VERSION_LIST = (
    rf"({VALID_VERSION_RANGE}|{VALID_VERSION})([,]({VALID_VERSION_RANGE}|{VALID_VERSION}))*"
)


class TokenKind(Enum):
    """Enumeration of the different token kinds in the spec grammar"""

    # FILENAME
    FILENAME = auto()
    # DAG hash
    DAG_HASH = auto()
    # Dependency
    DEPENDENCY = auto()
    # Version
    VERSION_HASH_PAIR = auto()
    VERSION = auto()
    # Variants
    PROPAGATED_BOOL_VARIANT = auto()
    BOOL_VARIANT = auto()
    KEY_VALUE_PAIR = auto()
    PROPAGATED_KEY_VALUE_PAIR = auto()
    # Compilers
    COMPILER_AND_VERSION = auto()
    COMPILER = auto()
    # Package name
    UNQUALIFIED_PACKAGE_NAME = auto()
    FULLY_QUALIFIED_PACKAGE_NAME = auto()
    # White spaces
    WS = auto()

    def __str__(self):
        return f"{self._name_}"


class Token:
    """Represents tokens; generated from input by lexer and fed to parse()."""

    __slots__ = "kind", "value", "start", "end"

    def __init__(
        self, kind: TokenKind, value: str, start: Optional[int] = None, end: Optional[int] = None
    ):
        self.kind = kind
        self.value = value
        self.start = start
        self.end = end

    def __repr__(self):
        return str(self)

    def __str__(self):
        return f"({self.kind}, {self.value})"

    def __eq__(self, other):
        return (self.kind == other.kind) and (self.value == other.value)


#: List of all the regexes used to match spec parts, in order of precedence
TOKEN_REGEXES = [
    # Dependency
    rf"(?P<{TokenKind.DEPENDENCY}>\^)",
    # Version regexes
    rf"(?P<{TokenKind.VERSION_HASH_PAIR}>@({VALID_GIT_VERSION}={VALID_VERSION}))",
    rf"(?P<{TokenKind.VERSION}>@({VALID_VERSION_LIST}))",
    # Variant regexes
    rf"(?P<{TokenKind.PROPAGATED_BOOL_VARIANT}>(\+\+|~~|--){VALID_NAME})",
    rf"(?P<{TokenKind.BOOL_VARIANT}>[~+-]{VALID_NAME})",
    rf"(?P<{TokenKind.PROPAGATED_KEY_VALUE_PAIR}>({VALID_NAME}==({VALID_VALUE}|{VALID_QUOTED_VALUE})))",  # noqa: E501
    rf"(?P<{TokenKind.KEY_VALUE_PAIR}>({VALID_NAME}=({VALID_VALUE}|{VALID_QUOTED_VALUE})))",
    # Compiler regexes
    rf"(?P<{TokenKind.COMPILER_AND_VERSION}>%({VALID_NAME})([\s]*)@({VALID_VERSION_LIST}))",
    rf"(?P<{TokenKind.COMPILER}>%({VALID_NAME}))",
    # Filename
    rf"(?P<{TokenKind.FILENAME}>({VALID_FILENAME}))",
    # Spec name regexes
    rf"(?P<{TokenKind.FULLY_QUALIFIED_PACKAGE_NAME}>{VALID_NAME_WITH_DOTS})",
    rf"(?P<{TokenKind.UNQUALIFIED_PACKAGE_NAME}>{VALID_NAME_WITHOUT_DOTS})",
    # DAG hash
    rf"(?P<{TokenKind.DAG_HASH}>/({VALID_HASH}))",
    # White spaces (the lowest priority)
    rf"(?P<{TokenKind.WS}>\s+)",
]

#: Maps a string representation to the corresponding token kind
STR_TO_TOKEN = {str(x): x for x in TokenKind}

MASTER_REGEX = re.compile("|".join(TOKEN_REGEXES))


def tokenize(text: str) -> Iterator[Token]:
    """Return a token generator from the text passed as input.

    Raises:
        SpecTokenizationError: if we can't tokenize anymore, but didn't reach the
            end of the input text.
    """
    scanner = MASTER_REGEX.scanner(text)  # type: ignore[attr-defined]
    match: Optional[re.Match] = None
    for match in iter(scanner.match, None):
        yield Token(
            STR_TO_TOKEN[match.lastgroup],  # type: ignore[attr-defined]
            match.group(),  # type: ignore[attr-defined]
            match.start(),  # type: ignore[attr-defined]
            match.end(),  # type: ignore[attr-defined]
        )

    if match is None and not text:
        # We just got an empty string
        return

    if match is None or match.end() != len(text):
        raise SpecTokenizationError(match, text)


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

    def accept(self, kind: TokenKind):
        """If the next token is of the specified kind, advance the stream and return True.
        Otherwise return False.
        """
        if self.next_token and self.next_token.kind == kind:
            self.advance()
            return True
        return False


class SpecParser:
    """Parse text into specs"""

    __slots__ = "literal_str", "ctx"

    def __init__(self, literal_str: str):
        self.literal_str = literal_str
        self.ctx = TokenContext(filter(lambda x: x.kind != TokenKind.WS, tokenize(literal_str)))

    def tokens(self) -> List[Token]:
        """Return the entire list of token from the initial text. White spaces are
        filtered out.
        """
        return list(filter(lambda x: x.kind != TokenKind.WS, tokenize(self.literal_str)))

    def next_spec(self, spec_buffer: Optional[spack.spec.Spec] = None) -> spack.spec.Spec:
        """Return the next spec parsed from text.

        Args:
            spec_buffer: buffer where to parse the spec. If None a new one
                will be created.

        Return
            The spec that was parsed
        """
        spec_buffer = spec_buffer or spack.spec.Spec()
        root_spec = SpecNodeParser(self.ctx).parse(spec_buffer)
        while True:
            if self.ctx.accept(TokenKind.DEPENDENCY):
                dependency = SpecNodeParser(self.ctx).parse(spack.spec.Spec())

                if dependency == spack.spec.Spec():
                    msg = "cannot parse a dependency sigil without a following dependency"
                    raise SpecParsingError(msg, self.ctx.current_token, self.literal_str)

                root_spec._add_dependency(dependency, ())

            else:
                break

        return root_spec

    def all_specs(self) -> List[spack.spec.Spec]:
        """Return all the specs that remain to be parsed"""
        return list(iter(self.next_spec, spack.spec.Spec()))


class SpecNodeParser:
    """Parse a single spec node from a stream of tokens"""

    __slots__ = "ctx", "has_compiler", "has_version"

    def __init__(self, ctx):
        self.ctx = ctx
        self.has_compiler = False
        self.has_version = False

    def parse(self, spec_buffer: spack.spec.Spec) -> spack.spec.Spec:
        """Parse a single spec node from a stream of tokens

        Args:
            spec_buffer: buffer where to parse the spec

        Return
            The buffer passed as argument
        """
        import spack.environment  # Needed to retrieve by hash

        # If we start with a package name we have a named spec, we cannot
        # accept another package name afterwards in a node
        if self.ctx.accept(TokenKind.UNQUALIFIED_PACKAGE_NAME):
            spec_buffer.name = self.ctx.current_token.value
        elif self.ctx.accept(TokenKind.FULLY_QUALIFIED_PACKAGE_NAME):
            parts = self.ctx.current_token.value.split(".")
            name = parts[-1]
            namespace = ".".join(parts[:-1])
            spec_buffer.name = name
            spec_buffer.namespace = namespace
        elif self.ctx.accept(TokenKind.FILENAME):
            return FileParser(self.ctx).parse(spec_buffer)

        while True:
            if self.ctx.accept(TokenKind.COMPILER):
                if self.has_compiler:
                    # TODO: Improve error reporting
                    raise spack.spec.DuplicateCompilerSpecError(
                        f"{spec_buffer} cannot have multiple compilers"
                    )

                compiler_name = self.ctx.current_token.value[1:]
                spec_buffer.compiler = spack.spec.CompilerSpec(compiler_name, ":")
                self.has_compiler = True
            elif self.ctx.accept(TokenKind.COMPILER_AND_VERSION):
                if self.has_compiler:
                    # TODO: Improve error reporting
                    raise spack.spec.DuplicateCompilerSpecError(
                        f"{spec_buffer} cannot have multiple compilers"
                    )

                compiler_name, compiler_version = self.ctx.current_token.value[1:].split("@")
                spec_buffer.compiler = spack.spec.CompilerSpec(compiler_name, compiler_version)
                self.has_compiler = True
            elif self.ctx.accept(TokenKind.VERSION) or self.ctx.accept(
                TokenKind.VERSION_HASH_PAIR
            ):
                if self.has_version:
                    # TODO: Improve error reporting here
                    raise spack.spec.MultipleVersionError(
                        f"{spec_buffer} cannot have multiple versions"
                    )

                version_list = spack.version.VersionList()
                version_list.add(spack.version.from_string(self.ctx.current_token.value[1:]))
                spec_buffer.versions = version_list

                # Add a git lookup method for GitVersions
                if (
                    spec_buffer.name
                    and spec_buffer.versions.concrete
                    and isinstance(spec_buffer.version, spack.version.GitVersion)
                ):
                    spec_buffer.version.generate_git_lookup(spec_buffer.fullname)

                self.has_version = True
            elif self.ctx.accept(TokenKind.BOOL_VARIANT):
                variant_value = self.ctx.current_token.value[0] == "+"
                spec_buffer._add_flag(
                    self.ctx.current_token.value[1:], variant_value, propagate=False
                )
            elif self.ctx.accept(TokenKind.PROPAGATED_BOOL_VARIANT):
                variant_value = self.ctx.current_token.value[0:2] == "++"
                spec_buffer._add_flag(
                    self.ctx.current_token.value[2:], variant_value, propagate=True
                )
            elif self.ctx.accept(TokenKind.KEY_VALUE_PAIR):
                name, value = self.ctx.current_token.value.split("=", maxsplit=1)
                value = value.strip("'\"")
                spec_buffer._add_flag(name, value, propagate=False)
            elif self.ctx.accept(TokenKind.PROPAGATED_KEY_VALUE_PAIR):
                name, value = self.ctx.current_token.value.split("==", maxsplit=1)
                value = value.strip("'\"")
                spec_buffer._add_flag(name, value, propagate=True)
            elif self.ctx.accept(TokenKind.DAG_HASH):
                dag_hash = self.ctx.current_token.value[1:]
                matches = []
                if spack.environment.active_environment():
                    matches = spack.environment.active_environment().get_by_hash(dag_hash)
                if not matches:
                    matches = spack.store.db.get_by_hash(dag_hash)
                if not matches:
                    raise spack.spec.NoSuchHashError(dag_hash)

                if len(matches) != 1:
                    raise spack.spec.AmbiguousHashError(
                        f"Multiple packages specify hash beginning '{dag_hash}'.", *matches
                    )
                spec_by_hash = matches[0]
                if not spec_by_hash.satisfies(spec_buffer):
                    raise spack.spec.InvalidHashError(spec_buffer, spec_by_hash.dag_hash())
                spec_buffer._dup(spec_by_hash)

                # When we receive an hash, and we checked that it matches the
                # literal constraint that people added in front of it, we need
                # to return it immediately
                return spec_buffer
            else:
                break

        return spec_buffer


class FileParser:
    """Parse a single spec from a JSON or YAML file"""

    __slots__ = ("ctx",)

    def __init__(self, ctx):
        self.ctx = ctx

    def parse(self, spec_buffer: spack.spec.Spec) -> spack.spec.Spec:
        """Parse a spec tree from a specfile.

        Args:
            spec_buffer: buffer where to parse the spec

        Return
            The buffer passed as argument
        """
        file = pathlib.Path(self.ctx.current_token.value)

        # TODO: Improve error messages
        if not file.exists():
            raise spack.spec.NoSuchSpecFileError(f"No such spec file: '{file}'")

        with file.open("r", encoding="utf-8") as stream:
            if str(file).endswith(".json"):
                spec_from_file = spack.spec.Spec.from_json(stream)
            else:
                spec_from_file = spack.spec.Spec.from_yaml(stream)
        spec_buffer._dup(spec_from_file)
        return spec_buffer


def parse(text: str) -> List[spack.spec.Spec]:
    """Parse text into a list of strings

    Args:
        text (str): text to be parsed

    Return:
        List of specs
    """
    return SpecParser(text).all_specs()


def parse_one_or_raise(
    text: str, spec_buffer: Optional[spack.spec.Spec] = None
) -> spack.spec.Spec:
    """Parse exactly one spec from text and return it, or raise

    Args:
        text (str): text to be parsed
        spec_buffer: buffer where to parse the spec. If None a new one will be created.
    """
    stripped_text = text.strip()
    parser = SpecParser(stripped_text)
    result = parser.next_spec(spec_buffer)
    last_token = parser.ctx.current_token

    if last_token is not None and last_token.end != len(stripped_text):
        message = "a single spec was requested, but parsed more than one:"
        message += f"\n{text}"
        if last_token is not None:
            underline = f"\n{' ' * last_token.end}{'^' * (len(text) - last_token.end)}"
            message += color.colorize(f"@*r{{{underline}}}")
        raise ValueError(message)

    return result


class SpecSyntaxError(Exception):
    """Base class for Spec syntax errors"""


class SpecTokenizationError(SpecSyntaxError):
    """Syntax error in a spec string"""

    def __init__(self, last_match, text):
        message = "cannot parse the current spec string\n"
        message += f"{text}"
        if last_match is not None:
            message += f"\n{' '*last_match.end()}{'^'*(len(text) - last_match.end())}"
        else:
            message += f"\n{'^' * len(text)}"
        super().__init__(message)


class SpecParsingError(SpecSyntaxError):
    """Error when parsing tokens"""

    def __init__(self, message, token, text):
        message += f"\n{text}"
        message += f"\n{' '*token.start}{'^'*(token.end - token.start)}"
        super().__init__(message)
