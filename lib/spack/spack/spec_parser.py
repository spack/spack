# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
"""Parser for spec literals

Here is the EBNF grammar for a spec::

    spec          = [name] [node_options] { sigil [edge_properties] dependency } |
                    [name] [node_options] hash |
                    filename

    sigil         = ^ | % | %%
    dependency    = virtual_assignment [node_options] | node
    node          =  name [node_options] |
                     [name] [node_options] hash |
                     filename

    node_options    = [@(version_list|version_pair)] { variant } [hash]
    edge_properties = [ { key_value } ]

    virtual_assignment = id { , id } = name
    hash          = / id
    filename      = (.|/|[a-zA-Z0-9-_]*/)([a-zA-Z0-9-_./]*)(.json|.yaml)

    name          = id | namespace id | *
    namespace     = { id . }

    variant       = bool_variant | key_value | propagated_bv | propagated_kv
    bool_variant  =  +id |  ~id |  -id
    propagated_bv = ++id | ~~id | --id
    key_value     =  id=id |  id=quoted_id
    propagated_kv = id==id | id==quoted_id

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

Identifiers using the ``<name>=<value>`` command, such as architectures and
compiler flags, require a space before the name.

There are two context-sensitive parts: ids in versions may contain ``.``, while other ids may
not; and a ``key=value`` pair directly after a dependency sigil or edge properties, where the
value is a package name, is a virtual assignment ``%c,cxx=gcc`` rather than a variant of an
anonymous dependency (write ``%*foo=bar`` for the latter). ``*`` is the name of an anonymous
node.

There is one ambiguity: since ``-`` is allowed in an id, you need to put
whitespace space before ``-variant`` for it to be tokenized properly.  You can
either use whitespace, or you can just use ``~variant`` since it means the same
thing.  Spack uses ``~variant`` in directory names and in the canonical form of
specs to avoid ambiguity.  Both are provided because ``~`` can cause shell
expansion when it is the first character in an id typed on the command line.
"""

import json
import pathlib
import re
import sys
from typing import TYPE_CHECKING, Dict, Iterator, List, Match, Optional, Tuple, Type, Union

import spack.deptypes
import spack.error
import spack.version
from spack.aliases import LEGACY_COMPILER_TO_BUILTIN
from spack.enums import PropagationPolicy
from spack.tokenize import Token, TokenBase, Tokenizer
from spack.util.tty import color

if TYPE_CHECKING:
    import spack.spec

#: Valid name for specs and variants. Here we are not using
#: the previous ``w[\w.-]*`` since that would match most
#: characters that can be part of a word in any language
IDENTIFIER = r"(?:[a-zA-Z_0-9][a-zA-Z_0-9\-]*)"
DOTTED_IDENTIFIER = rf"(?:{IDENTIFIER}(?:\.{IDENTIFIER})+)"
GIT_HASH = r"(?:[A-Fa-f0-9]{40})"
#: Git refs include branch names, and can contain ``.`` and ``/``
GIT_REF = r"(?:[a-zA-Z_0-9][a-zA-Z_0-9./\-]*)"
GIT_VERSION_PATTERN = rf"(?:(?:git\.(?:{GIT_REF}))|(?:{GIT_HASH}))"

STAR = r"\*"

#: Substitute a package for a virtual, e.g. ``c,cxx=gcc``. Overlaps with a key-value pair, and is
#: only tried first right after a dependency sigil or edge properties.
VIRTUAL_ASSIGNMENT = rf"(?:{IDENTIFIER}(?:,{IDENTIFIER})*=(?:{DOTTED_IDENTIFIER}|{IDENTIFIER}))"

NAME = r"[a-zA-Z_0-9][a-zA-Z_0-9\-.]*"

HASH = r"[a-zA-Z_0-9]+"

#: These are legal values that *can* be parsed bare, without quotes on the command line.
VALUE = r"(?:[a-zA-Z_0-9\-+\*.,:=%^\~\/\\]+)"

#: Quoted values can be *anything* in between quotes, including escaped quotes.
QUOTED_VALUE = r"(?:'(?:[^']|(?<=\\)')*'|\"(?:[^\"]|(?<=\\)\")*\")"

#: A version starts and ends with an alphanumeric character and is the whole run of version
#: characters, so a following ``=`` cannot be satisfied by backtracking into a shorter version.
VERSION = r"=?(?:[a-zA-Z0-9_](?:[a-zA-Z_0-9\-\.]*[a-zA-Z0-9_])?(?![a-zA-Z_0-9\-\.]))"
#: The upper bound of a range is not the key of a key-value pair: ``@1.2:develop=foo`` is ``@1.2:``
#: and a variant.
VERSION_RANGE = rf"(?:(?:{VERSION})?:(?:{VERSION}(?!\s*=))?)"
VERSION_LIST = rf"(?:{VERSION_RANGE}|{VERSION})(?:\s*,\s*(?:{VERSION_RANGE}|{VERSION}))*"

#: Split ``key=value]]`` into key, delimiter, value and closing brackets of edge attributes
SPLIT_KVP = re.compile(rf"^({NAME})(:?==?)(.*?)(\]*)$")

#: A filename starts either with a ``.`` or a ``/`` or a ``{name}/``, or on Windows, a drive letter
#: followed by a colon and ``\`` or ``.`` or ``{name}\``
WINDOWS_FILENAME = r"(?:\.|[a-zA-Z0-9-_]*\\|[a-zA-Z]:\\)(?:[a-zA-Z0-9-_\.\\]*)(?:\.json|\.yaml)"
UNIX_FILENAME = r"(?:\.|\/|[a-zA-Z0-9-_]*\/)(?:[a-zA-Z0-9-_\.\/]*)(?:\.json|\.yaml)"
FILENAME = WINDOWS_FILENAME if sys.platform == "win32" else UNIX_FILENAME

#: Regex to strip quotes. Group 2 will be the unquoted string.
STRIP_QUOTES = re.compile(r"^(['\"])(.*)\1$")

#: Values that match this (e.g., variants, flags) can be left unquoted in Spack output
NO_QUOTES_NEEDED = re.compile(r"^[a-zA-Z0-9,/_.\-]+$")


class SpecTokens(TokenBase):
    """Enumeration of the different token kinds of tokens in the spec grammar.

    Order of declaration is extremely important, since text containing specs is parsed with a
    single regex obtained by ``"|".join(...)`` of all the regex in the order of declaration.
    """

    # Dependency
    START_EDGE_PROPERTIES = r"(?:(?:\^|\%\%|\%)\[)"
    END_EDGE_PROPERTIES = r"(?:\])"
    DEPENDENCY = r"(?:\^|\%\%|\%)"

    # Version
    VERSION_HASH_PAIR = rf"(?:@(?:{GIT_VERSION_PATTERN})=(?:{VERSION}))"
    GIT_VERSION = rf"@(?:{GIT_VERSION_PATTERN})"
    VERSION = rf"(?:@\s*(?:{VERSION_LIST}))"

    # Variants
    PROPAGATED_BOOL_VARIANT = rf"(?:(?:\+\+|~~|--)\s*{NAME})"
    BOOL_VARIANT = rf"(?:[~+-]\s*{NAME})"
    PROPAGATED_KEY_VALUE_PAIR = rf"(?:{NAME}:?==(?:{VALUE}|{QUOTED_VALUE}))"
    KEY_VALUE_PAIR = rf"(?:{NAME}:?=(?:{VALUE}|{QUOTED_VALUE}))"

    # Virtual assignment, after KEY_VALUE_PAIR: only tried first at the start of a dependency
    VIRTUAL_ASSIGNMENT = rf"(?:{VIRTUAL_ASSIGNMENT})"

    # FILENAME
    FILENAME = rf"(?:{FILENAME})"

    # Package name
    FULLY_QUALIFIED_PACKAGE_NAME = rf"(?:{DOTTED_IDENTIFIER})"
    UNQUALIFIED_PACKAGE_NAME = rf"(?:{IDENTIFIER}|{STAR})"

    # DAG hash
    DAG_HASH = rf"(?:/(?:{HASH}))"

    # Unexpected character
    UNEXPECTED = r"\S"


#: Tokenizer that includes all the regexes in the SpecTokens enum. Whitespace between tokens is
#: skipped by the regex itself.
SPEC_TOKENIZER = Tokenizer(SpecTokens, skip_whitespace=True)

#: Right after a dependency sigil or edge properties, ``c,cxx=gcc`` is a virtual assignment
#: rather than a key-value pair. The tokenizer is context free, so this is matched separately.
_VIRTUAL_ASSIGNMENT_AHEAD = re.compile(rf"\s*({VIRTUAL_ASSIGNMENT})")

#: Tokens after which a dependency node starts
_NODE_START = (SpecTokens.DEPENDENCY, SpecTokens.END_EDGE_PROPERTIES)

#: The Spec class, imported on first use since ``spack.spec`` imports this module
_Spec: Optional[Type["spack.spec.Spec"]] = None


def _new_spec() -> "spack.spec.Spec":
    """Create an anonymous spec that matches anything"""
    global _Spec
    if _Spec is None:
        import spack.spec

        _Spec = spack.spec.Spec
    return _Spec()


def tokenize(text: str, *, everything: bool = False) -> Iterator[Token]:
    """Return a token generator from the text passed as input.

    Args:
        text: text to tokenize
        everything: if True, also yield unexpected tokens instead of raising

    Raises:
        SpecTokenizationError: when unexpected characters are found in the text
    """
    kinds, regex, pos = SPEC_TOKENIZER.kinds, SPEC_TOKENIZER.regex, 0
    while True:
        # The scanner is restarted after a virtual assignment, which is matched out of band
        scanner = regex.scanner(text, pos)  # type: ignore[attr-defined]
        for m in iter(scanner.match, None):
            kind = kinds[m.lastgroup]
            if kind is SpecTokens.UNEXPECTED and not everything:
                raise SpecTokenizationError(text)
            i = m.lastindex
            yield Token(kind, m.group(i), m.start(i), m.end(i))
            if kind in _NODE_START:
                va = _VIRTUAL_ASSIGNMENT_AHEAD.match(text, m.end())
                if va:
                    yield Token(SpecTokens.VIRTUAL_ASSIGNMENT, va.group(1), va.start(1), va.end())
                    pos = va.end()
                    break
        else:
            return


class SpecTokenizationError(spack.error.SpecSyntaxError):
    """Syntax error in a spec string"""

    def __init__(self, text: str):
        message = f"unexpected characters in the spec string\n{text}\n"

        underline = [" "] * len(text)
        for token in tokenize(text, everything=True):
            if token.kind is SpecTokens.UNEXPECTED:
                underline[token.start : token.end] = "^" * (token.end - token.start)

        message += color.colorize(f"@*r{{{''.join(underline).rstrip()}}}")
        super().__init__(message)


class SpecParser:
    """Parse text into specs.

    The parser drives the tokenizer regex directly, with one token of lookahead: ``self.curr``
    is the next token to consume, as a ``re.Match``, or ``None`` at the end of the input. The
    kind of that token is ``SPEC_TOKENIZER.kinds[self.curr.lastgroup]``, and its text is
    ``self.curr.group(self.curr.lastindex)``.

    A method call per token is comparatively expensive, so there are no ``accept`` and
    ``expect`` methods. Instead, the parser uses two idioms:

    * accept: after inspecting ``self.curr``, consume it with ``self.curr = self.scanner.match()``
    * expect: dispatch on the kind of ``self.curr``, and raise a parsing error from the branch
      where the token cannot appear at this point in the grammar
    """

    __slots__ = "literal_str", "scanner", "curr"

    def __init__(self, literal_str: str):
        self.literal_str = literal_str
        self.scanner = SPEC_TOKENIZER.regex.scanner(literal_str)  # type: ignore[attr-defined]
        self.curr = self.scanner.match()

    def tokens(self) -> List[Token]:
        """Return the entire list of token from the initial text."""
        return list(tokenize(self.literal_str))

    def next_spec(
        self, initial_spec: Optional["spack.spec.Spec"] = None
    ) -> Optional["spack.spec.Spec"]:
        """Return the next spec parsed from text.

        Args:
            initial_spec: object where to parse the spec. If None a new one
                will be created.

        Return:
            The spec that was parsed
        """
        if self.curr is None:
            return initial_spec

        # A ^ dependency is attached to the root only once its trailing % edges are parsed:
        # merging it earlier would compare an incomplete sub-dag against the existing edges.
        pending: Optional[Tuple["spack.spec.Spec", dict, Match]] = None

        first_token = self.curr
        root_spec = self._parse_node(initial_spec)
        current_spec = root_spec
        kinds = SPEC_TOKENIZER.kinds
        while self.curr is not None:
            token = self.curr
            kind = kinds[token.lastgroup]
            if kind is SpecTokens.DEPENDENCY:
                # ^ (transitive) or % / %% (direct) edge, followed by a dependency node
                edge_properties = {"virtuals": (), "depflag": 0}
            elif kind is SpecTokens.START_EDGE_PROPERTIES:
                # ^[key=value ...] or %[key=value ...] followed by a dependency node
                self.curr = self.scanner.match()
                edge_properties = self._parse_edge_properties()
            elif kind is SpecTokens.UNEXPECTED:
                raise SpecTokenizationError(self.literal_str)
            else:
                # Any other token starts the next spec in the input: this spec is complete
                break

            sigil = token.group(token.lastindex)
            edge_properties["direct"] = sigil[0] == "%"
            edge_properties["propagation"] = (
                PropagationPolicy.PREFERENCE if sigil.startswith("%%") else PropagationPolicy.NONE
            )

            dependency = self._parse_dependency(root_spec, edge_properties)
            is_direct = edge_properties["direct"]

            if is_direct:
                if dependency.name in LEGACY_COMPILER_TO_BUILTIN:
                    dependency.name = LEGACY_COMPILER_TO_BUILTIN[dependency.name]
                self._attach_dependency(current_spec, dependency, token, **edge_properties)
            else:
                self._attach_pending(root_spec, pending)
                current_spec = dependency
                pending = (dependency, edge_properties, token)

        self._attach_pending(root_spec, pending)

        if self.curr is not None and self.curr is first_token:
            raise SpecParsingError("unexpected token", self.curr, self.literal_str)

        return root_spec

    def _attach_pending(
        self,
        root_spec: "spack.spec.Spec",
        pending: Optional[Tuple["spack.spec.Spec", dict, Match]],
    ) -> None:
        """Attach the pending ^ dependency, whose sub-dag is complete now."""
        if pending is not None:
            dependency, edge_properties, token = pending
            self._attach_dependency(root_spec, dependency, token, **edge_properties)

    def _attach_dependency(
        self,
        target_spec: "spack.spec.Spec",
        dependency: "spack.spec.Spec",
        token: Match,
        **edge_properties,
    ) -> None:
        try:
            target_spec._add_dependency(dependency, **edge_properties)
        except spack.error.SpecError as e:
            raise SpecParsingError(str(e), token, self.literal_str) from e

    def _parse_edge_properties(self) -> dict:
        """Parse the ``key=value`` pairs of the edge properties, up to the closing bracket, and
        return them as keyword arguments for ``Spec._add_dependency``. The closing bracket is
        left as the current token, since a virtual assignment may follow it."""
        virtuals: Tuple[str, ...] = ()
        depflag = 0
        when = None
        kinds = SPEC_TOKENIZER.kinds
        while self.curr is not None:
            token = self.curr
            if kinds[token.lastgroup] is not SpecTokens.KEY_VALUE_PAIR:
                break
            self.curr = self.scanner.match()
            name, value = token.group(token.lastindex).split("=", maxsplit=1)
            name = name.rstrip(":")  # the := of a concrete variant has no meaning on an edge
            value = strip_quotes_and_unescape(value)
            if name == "virtuals":
                virtuals += tuple(value.split(","))
            elif name == "deptypes":
                depflag |= spack.deptypes.canonicalize(value.split(","))
            elif name == "when":
                # A when value is one spec string, where a comma is part of the syntax: when='@1,2'
                when = parse_one_or_raise(value)
            else:
                msg = (
                    "the only edge attributes that are currently accepted "
                    'are "deptypes", "virtuals", and "when"'
                )
                raise SpecParsingError(msg, token, self.literal_str)

        # TODO: Add code to accept bool variants here as soon as use variants are implemented
        if self.curr is None or kinds[self.curr.lastgroup] is not SpecTokens.END_EDGE_PROPERTIES:
            msg = "unexpected token in edge attributes"
            raise SpecParsingError(msg, self.curr, self.literal_str)

        edge_properties = {"virtuals": virtuals, "depflag": depflag}
        if when is not None:
            edge_properties["when"] = when
        return edge_properties

    def _parse_dependency(
        self, root_spec: "spack.spec.Spec", edge_properties: dict
    ) -> "spack.spec.Spec":
        """Parse the dependency node after the current token, which is a dependency sigil or the
        closing bracket of edge properties.

        A virtual assignment ``c,cxx=gcc`` right after them adds virtuals to the edge properties
        and names the node. The tokenizer is context free, so it is matched here, before the
        scanner is advanced past the current token, in the same way as in :func:`tokenize`.
        """
        assert self.curr is not None
        assignment = _VIRTUAL_ASSIGNMENT_AHEAD.match(self.literal_str, self.curr.end())
        if assignment is None:
            self.curr = self.scanner.match()
            dependency = self._parse_node()
        else:
            self.scanner = SPEC_TOKENIZER.regex.scanner(  # type: ignore[attr-defined]
                self.literal_str, assignment.end()
            )
            self.curr = self.scanner.match()

            virtuals, substitute = assignment.group(1).split("=")
            edge_properties["virtuals"] += tuple(virtuals.split(","))
            namespace, _, name = substitute.rpartition(".")
            dependency = _new_spec()
            dependency.name = name
            dependency.namespace = namespace or None
            self._parse_node_options(dependency)

        if root_spec.concrete:
            raise spack.error.SpecError(str(root_spec), "^" + str(dependency))
        return dependency

    def _parse_node(self, initial_spec: Optional["spack.spec.Spec"] = None) -> "spack.spec.Spec":
        """Parse a single spec node: an optional package name or spec file, and node options.

        Args:
            initial_spec: object to be constructed

        Return:
            The object passed as argument
        """
        if initial_spec is None:
            initial_spec = _new_spec()

        token = self.curr
        if token is None:
            return initial_spec

        # If we start with a package name we have a named spec, we cannot
        # accept another package name afterwards in a node
        kind = SPEC_TOKENIZER.kinds[token.lastgroup]
        if kind is SpecTokens.UNQUALIFIED_PACKAGE_NAME:
            name = token.group(token.lastindex)
            if name != "*":  # `*` is the name of an anonymous node, as in `%*+shared`
                initial_spec.name = name
            self.curr = self.scanner.match()

        elif kind is SpecTokens.FULLY_QUALIFIED_PACKAGE_NAME:
            initial_spec.namespace, initial_spec.name = token.group(token.lastindex).rsplit(".", 1)
            self.curr = self.scanner.match()

        elif kind is SpecTokens.FILENAME:
            self.curr = self.scanner.match()
            return self._parse_specfile(token.group(token.lastindex), initial_spec)

        return self._parse_node_options(initial_spec)

    def _parse_node_options(self, spec: "spack.spec.Spec") -> "spack.spec.Spec":
        """Parse the options of a node (version, variants, hash) into ``spec``"""
        kinds, scanner = SPEC_TOKENIZER.kinds, self.scanner
        has_version = False
        while self.curr is not None:
            token = self.curr
            kind = kinds[token.lastgroup]

            if (
                kind is SpecTokens.VERSION
                or kind is SpecTokens.GIT_VERSION
                or kind is SpecTokens.VERSION_HASH_PAIR
            ):
                if has_version:
                    raise SpecParsingError(
                        "Spec cannot have multiple versions", token, self.literal_str
                    )
                spec.versions = spack.version.VersionList(
                    [spack.version.from_string(token.group(token.lastindex)[1:])]
                )
                spec.attach_git_version_lookup()
                has_version = True
                self.curr = scanner.match()

            elif kind is SpecTokens.BOOL_VARIANT:
                value = token.group(token.lastindex)
                self._add_flag(spec, token, value[1:].strip(), value[0] == "+", False, True)
                self.curr = scanner.match()

            elif kind is SpecTokens.PROPAGATED_BOOL_VARIANT:
                value = token.group(token.lastindex)
                self._add_flag(spec, token, value[2:].strip(), value[:2] == "++", True, True)
                self.curr = scanner.match()

            elif kind is SpecTokens.KEY_VALUE_PAIR:
                name, value = token.group(token.lastindex).split("=", maxsplit=1)
                concrete = name.endswith(":")
                if concrete:
                    name = name[:-1]
                value = strip_quotes_and_unescape(value)
                self._add_flag(spec, token, name, value, False, concrete)
                self.curr = scanner.match()

            elif kind is SpecTokens.PROPAGATED_KEY_VALUE_PAIR:
                name, value = token.group(token.lastindex).split("==", maxsplit=1)
                concrete = name.endswith(":")
                if concrete:
                    name = name[:-1]
                value = strip_quotes_and_unescape(value)
                self._add_flag(spec, token, name, value, True, concrete)
                self.curr = scanner.match()

            elif kind is SpecTokens.DAG_HASH:
                if spec.abstract_hash:
                    # A second hash belongs to the next spec, e.g. `spack find /abc /def`
                    break
                spec.abstract_hash = token.group(token.lastindex)[1:]
                self.curr = scanner.match()

            elif kind is SpecTokens.VIRTUAL_ASSIGNMENT:
                raise SpecParsingError(
                    "a virtual assignment such as c,cxx=gcc must directly follow a dependency "
                    "sigil (^ or %) or edge properties",
                    token,
                    self.literal_str,
                )

            else:
                # A dependency sigil, edge properties, package name, spec file or unexpected
                # character: this node is done, and the caller decides what is valid next
                break

        return spec

    def _add_flag(
        self,
        spec: "spack.spec.Spec",
        token: Match,
        name: str,
        value: Union[str, bool],
        propagate: bool,
        concrete: bool,
    ) -> None:
        """Wrapper around ``Spec._add_flag()`` that adds parser context to errors raised."""
        try:
            spec._add_flag(name, value, propagate, concrete)
        except Exception as e:
            raise SpecParsingError(str(e), token, self.literal_str) from e

    def _parse_specfile(self, filename: str, initial_spec: "spack.spec.Spec") -> "spack.spec.Spec":
        """Parse a spec tree from a JSON or YAML spec file into ``initial_spec``"""
        file = pathlib.Path(filename)

        if not file.exists():
            raise spack.error.NoSuchSpecFileError(f"No such spec file: '{file}'")

        from spack.spec import Spec

        with file.open("r", encoding="utf-8") as stream:
            if str(file).endswith(".json"):
                spec_from_file = Spec.from_json(stream)
            else:
                spec_from_file = Spec.from_yaml(stream)
        initial_spec._dup(spec_from_file)
        return initial_spec

    def all_specs(self) -> List["spack.spec.Spec"]:
        """Return all the specs that remain to be parsed"""
        return list(iter(self.next_spec, None))


def parse(text: str, *, toolchains: Optional[Dict] = None) -> List["spack.spec.Spec"]:
    """Parse text into a list of specs

    Args:
        text: text to be parsed
        toolchains: optional toolchain definitions to expand after parsing

    Return:
        List of specs
    """
    specs = SpecParser(text).all_specs()
    if toolchains:
        cache: Dict[str, "spack.spec.Spec"] = {}
        for spec in specs:
            expand_toolchains(spec, toolchains, _cache=cache)
    return specs


def parse_one_or_raise(
    text: str,
    initial_spec: Optional["spack.spec.Spec"] = None,
    *,
    toolchains: Optional[Dict] = None,
) -> "spack.spec.Spec":
    """Parse exactly one spec from text and return it, or raise

    Args:
        text: text to be parsed
        initial_spec: buffer where to parse the spec. If None a new one will be created.
        toolchains: optional toolchain definitions to expand after parsing
    """
    parser = SpecParser(text)
    result = parser.next_spec(initial_spec)

    if parser.curr is not None:
        message = f"expected a single spec, but got more:\n{text}"
        message += color.colorize(f"@*r{{{_underline(parser.curr)}}}")
        raise ValueError(message)

    if result is None:
        raise ValueError("expected a single spec, but got none")

    if toolchains:
        expand_toolchains(result, toolchains)

    return result


def _parse_toolchain_config(toolchain_config: Union[str, List[Dict]]) -> "spack.spec.Spec":
    """Parse a toolchain config entry (string or list) into a Spec."""
    if isinstance(toolchain_config, str):
        toolchain = parse_one_or_raise(toolchain_config)
        _ensure_all_direct_edges(toolchain)
    else:
        from spack.spec import EMPTY_SPEC, Spec

        toolchain = Spec()
        for entry in toolchain_config:
            toolchain_part = parse_one_or_raise(entry["spec"])
            when = entry.get("when", "")
            _ensure_all_direct_edges(toolchain_part)

            if when:
                when_spec = Spec(when)
                for edge in toolchain_part.traverse_edges():
                    if edge.when is EMPTY_SPEC:
                        edge.when = when_spec.copy()
                    else:
                        edge.when.constrain(when_spec)
            toolchain.constrain(toolchain_part)
    return toolchain


def _ensure_all_direct_edges(constraint: "spack.spec.Spec") -> None:
    """Validate that a toolchain spec only has direct (%) edges."""
    for edge in constraint.traverse_edges(root=False):
        if not edge.direct:
            raise spack.error.SpecError(
                f"cannot use '^' in toolchain definitions, and the current "
                f"toolchain contains '{edge.format()}'"
            )


def expand_toolchains(
    spec: "spack.spec.Spec",
    toolchains: Dict,
    *,
    _cache: Optional[Dict[str, "spack.spec.Spec"]] = None,
) -> None:
    """Replace toolchain placeholder deps with expanded toolchain constraints.

    Walks every node in the spec DAG. For each node, finds direct dependency
    edges whose child name is a key in ``toolchains``. Removes the placeholder
    edge, parses the toolchain config, copies with the edge's propagation
    policy, and constrains the node.
    """
    if _cache is None:
        _cache = {}

    for node in list(spec.traverse()):
        for edge in list(node.edges_to_dependencies()):
            if not edge.direct:
                continue
            name = edge.spec.name
            if name not in toolchains:
                continue

            # Remove the placeholder edge (both directions)
            node._dependencies[name].remove(edge)
            if not node._dependencies[name]:
                del node._dependencies[name]
            edge.spec._dependents[node.name].remove(edge)
            if not edge.spec._dependents[node.name]:
                del edge.spec._dependents[node.name]

            # Parse and cache toolchain
            if name not in _cache:
                _cache[name] = _parse_toolchain_config(toolchains[name])

            propagation = edge.propagation
            propagation_arg = None if propagation != PropagationPolicy.PREFERENCE else propagation
            # Copy so each usage gets a distinct object (solver depends on this)
            toolchain = _cache[name].copy(propagation=propagation_arg)
            node.constrain(toolchain)


def _underline(token: Match) -> str:
    """Return a line that underlines the token in the spec string above it"""
    start, end = token.span(token.lastindex or 0)
    return f"\n{' ' * start}{'^' * (end - start)}"


class SpecParsingError(spack.error.SpecSyntaxError):
    """Error when parsing tokens"""

    def __init__(self, message: str, token: Optional[Match], text: str):
        message += f"\n{text}"
        if token is not None:
            message += color.colorize(f"@*r{{{_underline(token)}}}")
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
