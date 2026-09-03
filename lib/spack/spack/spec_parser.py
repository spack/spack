# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
"""Parser for spec literals

Here is the EBNF grammar for a spec::

    spec          = node { sigil [edge_properties] dependency }

    sigil         = ^ | % | %%
    dependency    = virtual_assignment { node_option } | node
    node          = [name] { node_option } | filename
    node_option   = @version_list | @version_pair | variant | hash

    edge_properties = [ { key_value | when=quoted_spec } [ when=spec ] ]
    quoted_spec     = " spec " | ' spec '

    virtual_assignment = id { , id } = (id | namespace id)
    hash          = / [a-zA-Z0-9_]+
    filename      = (.|/|[a-zA-Z0-9-_]*/)([a-zA-Z0-9-_./]*)(.json|.yaml)

    name          = id | namespace id | *
    namespace     = id . { id . }

    variant       = bool_variant | key_value | propagated_bv | propagated_kv
    bool_variant  = +id | ~id | -id
    propagated_bv = ++id | ~~id | --id
    key_value     = id=value | id:=value
    propagated_kv = id==value | id:==value
    value         = bare_value | quoted_value
    bare_value    = [a-zA-Z0-9_\\-+*.,:=%^~/\\\\]+
    quoted_value  = " [^"]* " | ' [^']* '

    version_pair  = git_version=vid
    version_list  = (version|version_range) { , (version|version_range) }
    version_range = [vid] : [vid]
    version       = [=] vid

    git_version   = git.(ref) | git_hash
    git_hash      = [A-Fa-f0-9]{40}
    ref           = [a-zA-Z0-9_][a-zA-Z_0-9-./]*
    vid           = [a-zA-Z0-9_] [ [a-zA-Z_0-9-.]* [a-zA-Z0-9_] ]
    id            = [a-zA-Z0-9_][a-zA-Z_0-9-]*

The options of a node come in any order, with at most one version and one hash: a second hash
starts the next spec, as in ``spack find /abc /def``. ``:=`` marks a concrete variant value, and
``==`` or ``:==`` propagate the value to dependencies.

Identifiers using the ``<name>=<value>`` command, such as architectures and
compiler flags, require a space before the name.

There are two context-sensitive parts: ids in versions may contain ``.``, while other ids may
not; and a ``key=value`` pair directly after a dependency sigil or edge properties, where the
value is a package name, is a virtual assignment ``%c,cxx=gcc`` rather than a variant of an
anonymous dependency (write ``%* foo=bar`` for the latter). ``*`` is the name of an anonymous
node.

The ``when=`` edge property is a condition on the edge, and its value is a spec that extends up
to the closing bracket, so it must be the last edge property: ``^[virtuals=mpi when=+mpi] mpich``.
A quoted condition, ``^[when='+mpi' virtuals=mpi] mpich``, is a value like any other and can
precede other edge properties.

There is one ambiguity: since ``-`` is allowed in an id, you need to put
whitespace space before ``-variant`` for it to be tokenized properly.  You can
either use whitespace, or you can just use ``~variant`` since it means the same
thing.  Spack uses ``~variant`` in directory names and in the canonical form of
specs to avoid ambiguity.  Both are provided because ``~`` can cause shell
expansion when it is the first character in an id typed on the command line.
"""

import os
import re
import sys
from typing import TYPE_CHECKING, Dict, List, Optional, Tuple, Type, Union

import spack.deptypes
import spack.error
import spack.version
from spack.aliases import LEGACY_COMPILER_TO_BUILTIN
from spack.enums import PropagationPolicy
from spack.tokenize import fast_regex
from spack.util.tty import color

if TYPE_CHECKING:
    import spack.spec

# Cannot use from spack.spec import Spec due to circularities, so we lazily
# import it inline and bind it here to avoid expensive local imports
Spec: Optional[Type["spack.spec.Spec"]] = None

#: Valid name for specs and variants. Here we are not using
#: the previous ``w[\w.-]*`` since that would match most
#: characters that can be part of a word in any language
IDENTIFIER = r"(?:[a-zA-Z_0-9][a-zA-Z_0-9\-]*)"
DOTTED_IDENTIFIER = rf"(?:{IDENTIFIER}(?:\.{IDENTIFIER})+)"
GIT_HASH = r"(?:[A-Fa-f0-9]{40})"
#: Git refs include branch names, and can contain ``.`` and ``/``
GIT_REF = r"(?:[a-zA-Z_0-9][a-zA-Z_0-9./\-]*)"
GIT_VERSION_PATTERN = rf"(?:(?:git\.(?:{GIT_REF}))|(?:{GIT_HASH}))"
#: A package name, optionally with a namespace
PACKAGE_NAME = rf"(?:{DOTTED_IDENTIFIER}|{IDENTIFIER})"

STAR = r"\*"

NAME = r"[a-zA-Z_0-9][a-zA-Z_0-9\-.]*"

HASH = r"[a-zA-Z_0-9]+"

#: These are legal values that *can* be parsed bare, without quotes on the command line.
VALUE = r"(?:[a-zA-Z_0-9\-+\*.,:=%^\~\/\\]+)"

#: Quoted values can be anything in between quotes, except the quote itself. There is no escaping.
QUOTED_VALUE = r"(?:'[^']*'|\"[^\"]*\")"

#: A version starts and ends with an alphanumeric character and is the whole run of version
#: characters, so a following ``=`` cannot be satisfied by backtracking into a shorter version.
VERSION = r"=?(?:[a-zA-Z0-9_](?:[a-zA-Z_0-9\-\.]*[a-zA-Z0-9_])?(?![a-zA-Z_0-9\-\.]))"
#: The upper bound of a range is not the key of a key-value pair, so ``@1.2:develop=foo`` is
#: ``@1.2:`` and a variant.
VERSION_RANGE = rf"(?:(?:{VERSION})?:(?:{VERSION}(?!\s*=))?)"
VERSION_LIST = rf"(?:{VERSION_RANGE}|{VERSION})(?:\s*,\s*(?:{VERSION_RANGE}|{VERSION}))*"

#: Split ``key=value]]`` into key, delimiter, value and closing brackets of edge attributes
SPLIT_KVP = re.compile(rf"^({NAME})(:?==?)(.*?)(\]*)$")

#: A filename starts either with a ``.`` or a ``/`` or a ``{name}/``, or on Windows, a drive letter
#: followed by a colon and ``\`` or ``.`` or ``{name}\``
WINDOWS_FILENAME = r"(?:\.|[a-zA-Z0-9-_]*\\|[a-zA-Z]:\\)(?:[a-zA-Z0-9-_\.\\]*)(?:\.json|\.yaml)"
UNIX_FILENAME = r"(?:\.|\/|[a-zA-Z0-9-_]*\/)(?:[a-zA-Z0-9-_\.\/]*)(?:\.json|\.yaml)"
FILENAME = WINDOWS_FILENAME if sys.platform == "win32" else UNIX_FILENAME

#: Values that match this (e.g., variants, flags) can be left unquoted in Spack output
NO_QUOTES_NEEDED = re.compile(r"^[a-zA-Z0-9,/_.\-]+$")


class SpecTokenizationError(spack.error.SpecSyntaxError):
    """Syntax error in a spec string"""

    def __init__(self, text: str) -> None:
        message = f"unexpected characters in the spec string\n{text}\n"

        # collect all tokens, and underline those that are unexpected
        scanner = FAST_SPEC_REGEX.scanner(text)  # type: ignore[attr-defined]

        # offset of unexpected token. unexpect tokens always have length 1.
        unexpected_indices: List[int] = []
        while True:
            match = scanner.match()
            if not match:
                break
            elif match.lastgroup == _UNEXPECTED:
                unexpected_indices.append(match.start(match.lastgroup))

        underline = ""
        last_index = 0
        for index in unexpected_indices:
            underline += " " * (index - last_index) + "^"
            last_index = index + 1

        message += color.colorize(f"@*r{{{underline}}}")
        super().__init__(message)


def parse(text: str, *, toolchains: Optional[Dict] = None) -> List["spack.spec.Spec"]:
    """Parse text into a list of strings

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

    if parser.curr:
        message = f"expected a single spec, but got more:\n{text}"
        start = parser.curr.start()
        end = parser.curr.end()
        # Adjust start to skip leading whitespace in the match
        matched_text = parser.curr.group()
        stripped_text = matched_text.lstrip()
        start += len(matched_text) - len(stripped_text)
        underline = f"\n{' ' * start}{'^' * (end - start)}"
        message += color.colorize(f"@*r{{{underline}}}")
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


class SpecParsingError(spack.error.SpecSyntaxError):
    """Error when parsing tokens"""

    def __init__(self, message: str, token, text: str):
        message += f"\n{text}"
        if token:
            start, end = token.span(token.lastgroup or 0)
            underline = f"\n{' ' * start}{'^' * (end - start)}"
            message += color.colorize(f"@*r{{{underline}}}")
        super().__init__(message)


def strip_quotes(string: str) -> str:
    """Remove surrounding single or double quotes from string, if present."""
    if len(string) >= 2 and string[0] in "'\"" and string[-1] == string[0]:
        return string[1:-1]
    return string


def quote_if_needed(value: str) -> str:
    """Add quotes around the value if it requires quotes, i.e. unless it matches
    :data:`NO_QUOTES_NEEDED`. Single quotes are used, or double quotes around a value that
    contains single quotes. There is no escaping: a value that contains both kinds of quotes
    cannot be written in a spec string.

    Raises:
        spack.error.SpecSyntaxError: if the value contains both single and double quotes
    """
    if NO_QUOTES_NEEDED.match(value):
        return value
    if "'" not in value:
        return f"'{value}'"
    if '"' not in value:
        return f'"{value}"'
    raise spack.error.SpecSyntaxError(
        f"cannot quote the value {value!r}: it contains both single and double quotes"
    )


# Token kinds: names of the top-level capture groups in FAST_SPEC_REGEX, compared against
# match.lastgroup in the parser.
_END_EDGE_PROPERTIES = "END_EDGE_PROPERTIES"
_DEPENDENCY = "DEPENDENCY"
_VERSION = "VERSION"
_BOOL_VARIANT = "BOOL_VARIANT"
_KEY_VALUE_PAIR = "KEY_VALUE_PAIR"
_WHEN = "WHEN"
_FILENAME = "FILENAME"
_FULLY_QUALIFIED_PACKAGE_NAME = "FULLY_QUALIFIED_PACKAGE_NAME"
_UNQUALIFIED_PACKAGE_NAME = "UNQUALIFIED_PACKAGE_NAME"
_DAG_HASH = "DAG_HASH"
_UNEXPECTED = "UNEXPECTED"

# Subgroup names within the token regexes below, read with match.group(...). All group names
# must be unique across FAST_SPEC_REGEX; re.compile enforces this.
_EDGE_BRACKET = "edge_bracket"
_EDGE_VIRTUALS = "edge_virtuals"
_EDGE_SUBSTITUTE = "edge_substitute"
_END_EDGE_VIRTUALS = "end_edge_virtuals"
_END_EDGE_SUBSTITUTE = "end_edge_substitute"
_GIT_VERSION = "git_version"
_VERSION_LIST = "version_list"
_BV_PREFIX = "bv_prefix"
_BV_NAME = "bv_name"
_KV_NAME = "kv_name"
_KV_SEP = "kv_sep"
_KV_VALUE = "kv_value"

# The virtual assignment ``c,cxx=gcc`` substitutes a package for one or more virtuals. Both
# END_EDGE_PROPERTIES and DEPENDENCY embed it, each with its own group names; only that context
# distinguishes it from KEY_VALUE_PAIR. It applies only if the whole value is a package name,
# i.e. the substitute is followed by whitespace, a variant, version or hash of the node, a sigil,
# a closing bracket, or the end of the input. Otherwise the pair is a variant of an anonymous
# node, e.g. ``^foo=bar:baz``, and the sigil is a token of its own.
_VIRTUALS_LIST = rf"{IDENTIFIER}(?:,{IDENTIFIER})*"  # comma-separated virtuals
_SUBSTITUTE_END = r"(?=\s|[+~]{1,2}\s*[a-zA-Z_0-9]|[@/^%\]]|$)"
_SUBSTITUTE = rf"{PACKAGE_NAME}{_SUBSTITUTE_END}"  # package to substitute for them

#: A virtual assignment outside a dependency, ``zlib c,cxx=gcc``, fails to tokenize at the comma:
#: matched on that error path only, so that it costs nothing in the token regex
_MISPLACED_VIRTUAL_ASSIGNMENT = re.compile(rf"{_VIRTUALS_LIST}={_SUBSTITUTE}")

#: Token kind -> regex. FAST_SPEC_REGEX is the ``|``-alternation of these in order: tokens are
#: tried top to bottom, so more specific tokens come first (e.g. FILENAME before package names).
SPEC_TOKENS: Dict[str, str] = {
    # ``]`` closing edge properties, optionally fused with a virtual assignment, e.g.
    # ``^[deptypes=link] mpi=openmpi``
    _END_EDGE_PROPERTIES: (
        r"\]"
        rf"(?:\s*(?P<{_END_EDGE_VIRTUALS}>{_VIRTUALS_LIST})=(?P<{_END_EDGE_SUBSTITUTE}>{_SUBSTITUTE}))?"
    ),
    # ``^`` (transitive), ``%`` (direct) or ``%%`` (direct, propagated) dependency
    _DEPENDENCY: (
        r"(?:\^|\%\%|\%)"
        r"(?:"
        rf"(?P<{_EDGE_BRACKET}>\[)"  # start of edge properties, e.g. ``^[virtuals=mpi]``
        rf"|(?:\s*(?P<{_EDGE_VIRTUALS}>{_VIRTUALS_LIST})=(?P<{_EDGE_SUBSTITUTE}>{_SUBSTITUTE}))?"
        r")"
    ),
    # ``@`` followed by a git version or a version list
    _VERSION: (
        rf"@(?:(?P<{_GIT_VERSION}>{GIT_VERSION_PATTERN}(?:={VERSION})?)"
        rf"|\s*(?P<{_VERSION_LIST}>{VERSION_LIST}))"
    ),
    # boolean variant, e.g. ``+debug``, ``~qt_4``, or propagated, e.g. ``++debug``
    _BOOL_VARIANT: (
        rf"(?P<{_BV_PREFIX}>\+\+|~~|--|[~+-])"  # propagated (``++``/``~~``/``--``) or plain
        r"\s*"
        rf"(?P<{_BV_NAME}>{NAME})"  # variant name
    ),
    # key-value pair, e.g. ``foo=bar``, ``foo==bar`` (propagated), ``foo:=bar`` (concrete)
    _KEY_VALUE_PAIR: (
        rf"(?P<{_KV_NAME}>{NAME})"  # key
        rf"(?P<{_KV_SEP}>:?==?)"  # separator: ``=``, ``==``, ``:=`` or ``:==``
        rf"(?P<{_KV_VALUE}>{VALUE}|{QUOTED_VALUE})"  # bare or quoted value
    ),
    # ``when=`` of edge properties whose spec is not a value, e.g. ``^[when=@1.2] dep``; otherwise
    # ``when=+foo`` is a key-value pair like any other, and ``when`` a variant name elsewhere
    _WHEN: r"when=",
    # path to a spec file, e.g. ``./foo/bar.json``
    _FILENAME: FILENAME,
    # package name with namespace, e.g. ``builtin.mpich``
    _FULLY_QUALIFIED_PACKAGE_NAME: DOTTED_IDENTIFIER,
    # package name, e.g. ``mpich``, or ``*`` for any package
    _UNQUALIFIED_PACKAGE_NAME: rf"(?:{IDENTIFIER}|{STAR})",
    # ``/`` followed by a (prefix of a) DAG hash
    _DAG_HASH: rf"/{HASH}",
    # anything else is a single unexpected character
    _UNEXPECTED: r".",
}

#: Single regex matching any spec token (and its subgroups) after optional whitespace
FAST_SPEC_REGEX = fast_regex(SPEC_TOKENS)


class SpecParser:
    """Fast spec parser using a single compiled regex.

    The parser operates directly on the stream of ``re.Match`` objects produced by
    ``FAST_SPEC_REGEX.scanner``, with one token of lookahead: ``self.curr`` is the current,
    not yet consumed token and ``self.next`` the one after it; both are ``None`` at the end
    of input. For a match, ``match.lastgroup`` is the token kind (a key of
    :data:`SPEC_TOKENS`), and subgroups of that token are accessed by name, e.g.
    ``match.group(_KV_NAME)``.

    Instead of ``accept``/``expect`` methods, the parser uses two idioms:

    * accept: after inspecting ``self.curr``, consume it by shifting the lookahead::

          self.curr, self.next = self.next, self.scanner.match()

    * expect: branch on ``self.curr.lastgroup``, and raise a parsing error from the branch
      where the token cannot appear at the current point in the grammar.
    """

    __slots__ = "literal_str", "scanner", "curr", "next"

    def __init__(self, literal_str: str):
        self.literal_str = literal_str.rstrip()
        self.scanner = FAST_SPEC_REGEX.scanner(self.literal_str)  # type: ignore[attr-defined]
        self.curr = self.scanner.match()
        self.next = self.scanner.match()

    def tokens(self, with_subgroups: bool = False) -> List[Tuple[str, str, Dict[str, str]]]:
        """Tokenize the spec string into a list of (kind, match, subgroups) tuples."""
        tokens: List[Tuple[str, str, Dict[str, str]]] = []
        scanner = FAST_SPEC_REGEX.scanner(self.literal_str)  # type: ignore[attr-defined]
        match = scanner.match()
        while match:
            kind = match.lastgroup
            if kind == _UNEXPECTED:
                self._raise_tokenization_error()
            full_match = match.group(match.lastgroup)
            if with_subgroups:
                subgroups = {
                    k: v for k, v in match.groupdict().items() if v is not None and k != kind
                }
            else:
                subgroups = {}
            tokens.append((kind, full_match, subgroups))
            match = scanner.match()
        return tokens

    def _raise_tokenization_error(self) -> None:
        # A virtual assignment outside a dependency, `zlib c,cxx=gcc`, fails at the comma: point
        # out the mistake instead of underlining the comma
        if self.curr is not None and self.curr.group(_UNEXPECTED) == ",":
            comma = self.curr.start(_UNEXPECTED)
            for assignment in _MISPLACED_VIRTUAL_ASSIGNMENT.finditer(self.literal_str):
                if assignment.start() <= comma < assignment.end():
                    raise SpecParsingError(
                        "a virtual assignment such as c,cxx=gcc must directly follow a "
                        "dependency sigil (^ or %) or edge properties",
                        assignment,
                        self.literal_str,
                    )
        raise SpecTokenizationError(self.literal_str)

    def _raise_parsing_error(self, message: str) -> None:
        raise SpecParsingError(message, self.curr, self.literal_str)

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
        if not self.curr:
            return initial_spec

        if self.curr.lastgroup == _UNEXPECTED:
            self._raise_tokenization_error()

        first_token = self.curr
        root_spec = self._parse_node(initial_spec)
        current_spec = root_spec

        # A ^ dependency is attached to the root only once its trailing % edges are parsed:
        # merging it earlier would compare an incomplete sub-dag against the existing edges.
        pending: Optional[tuple] = None

        while self.curr:
            if self.curr.lastgroup == _DEPENDENCY:
                # ^ (transitive) or % / %% (direct) edge, followed by a dependency node
                token = self.curr.group()
                # Strip leading whitespace for checking startswith
                token = token.lstrip()
                is_direct = token.startswith("%")
                propagation = PropagationPolicy.NONE
                if is_direct and token.startswith("%%"):
                    propagation = PropagationPolicy.PREFERENCE

                if self.curr.group(_EDGE_BRACKET):
                    # Bracketed form with edge properties: ^[key=value ...] node.
                    # Accept the opening ^[ / %[ token
                    self.curr, self.next = self.next, self.scanner.match()

                    # Collect edge attributes (key=value pairs) up to the closing bracket
                    attributes: Dict[str, List[str]] = {}
                    conditions: Optional["spack.spec.Spec"] = None
                    substitute = None
                    while True:
                        if not self.curr:
                            self._raise_parsing_error("unexpected token in edge attributes")

                        kind = self.curr.lastgroup
                        name = self.curr.group(_KV_NAME) if kind == _KEY_VALUE_PAIR else "when"

                        if kind == _KEY_VALUE_PAIR and name != "when":
                            if name not in ("deptypes", "virtuals"):
                                msg = (
                                    "the only edge attributes that are currently accepted are "
                                    '"deptypes", "virtuals", and a "when=<spec>" condition, '
                                    "which must be the last unless quoted"
                                )
                                self._raise_parsing_error(msg)
                            value = strip_quotes(self.curr.group(_KV_VALUE))
                            attributes[name] = [v.strip() for v in value.split(",")]
                            self.curr, self.next = self.next, self.scanner.match()

                        elif kind == _KEY_VALUE_PAIR or kind == _WHEN:
                            # The condition is a spec. Quoted, it is a value like any other pair.
                            # Unquoted, it extends up to the closing bracket: the tokenizer is
                            # context free, so restart the scanner at the value, which is either
                            # that of the pair or what follows a bare WHEN token (when=@1.2).
                            value = self.curr.group(_KV_VALUE) if kind == _KEY_VALUE_PAIR else ""
                            if value[:1] in ("'", '"'):
                                try:
                                    condition = parse_one_or_raise(strip_quotes(value))
                                except ValueError:
                                    msg = "expected a single spec as the when= condition"
                                    self._raise_parsing_error(msg)
                                self.curr, self.next = self.next, self.scanner.match()
                            else:
                                if not value and (
                                    not self.next or self.next.lastgroup == _END_EDGE_PROPERTIES
                                ):
                                    self._raise_parsing_error("expected a spec after when=")
                                self._rescan(
                                    self.curr.start(_KV_VALUE) if value else self.curr.end()
                                )
                                parsed = self.next_spec()
                                assert parsed is not None  # there is a token, so there is a spec
                                condition = parsed
                            # Repeated attributes combine: conditions are constrained, like
                            # virtuals accumulate and deptypes are or-ed
                            if conditions is None:
                                conditions = condition
                            else:
                                conditions.constrain(condition)

                        elif kind == _END_EDGE_PROPERTIES:
                            # Closing ], optionally fused with a virtual assignment, as in
                            # ^[deptypes=link] mpi=openmpi
                            virtuals_str = self.curr.group(_END_EDGE_VIRTUALS)
                            substitute = self.curr.group(_END_EDGE_SUBSTITUTE)

                            if virtuals_str:
                                virtuals = attributes.get("virtuals", [])
                                virtuals.extend(virtuals_str.split(","))
                                attributes["virtuals"] = virtuals

                            # Accept the ] token and stop collecting edge attributes
                            self.curr, self.next = self.next, self.scanner.match()

                            break
                        else:
                            # Only key=value pairs can occur between brackets
                            self._raise_parsing_error("unexpected token in edge attributes")

                    depflag = 0
                    if "deptypes" in attributes:
                        depflag = spack.deptypes.canonicalize(attributes["deptypes"])

                    virtuals_tuple = tuple(attributes.get("virtuals", ()))

                    dep_spec = self._parse_node(initial_name=substitute)

                    edge_kwargs = {
                        "direct": is_direct,
                        "depflag": depflag,
                        "virtuals": virtuals_tuple,
                        "propagation": propagation,
                        "when": conditions,
                    }
                    if is_direct:
                        if dep_spec.name in LEGACY_COMPILER_TO_BUILTIN:
                            dep_spec.name = LEGACY_COMPILER_TO_BUILTIN[dep_spec.name]
                        self._attach_dependency(current_spec, dep_spec, self.curr, edge_kwargs)
                    else:
                        self._attach_pending(root_spec, pending)
                        current_spec = dep_spec
                        pending = (dep_spec, self.curr, edge_kwargs)

                else:
                    # Plain form without brackets: ^node / %node, where the edge token may
                    # carry a virtual assignment, as in %c,cxx=gcc
                    virtuals_str = self.curr.group(_EDGE_VIRTUALS)
                    substitute = self.curr.group(_EDGE_SUBSTITUTE)

                    virtuals_tuple = tuple(virtuals_str.split(",")) if virtuals_str else ()

                    # Accept the ^ / % / %% token
                    self.curr, self.next = self.next, self.scanner.match()

                    dep_spec = self._parse_node(initial_name=substitute)

                    edge_kwargs = {
                        "direct": is_direct,
                        "depflag": 0,
                        "virtuals": virtuals_tuple,
                        "propagation": propagation,
                    }
                    if is_direct:
                        if dep_spec.name in LEGACY_COMPILER_TO_BUILTIN:
                            dep_spec.name = LEGACY_COMPILER_TO_BUILTIN[dep_spec.name]
                        self._attach_dependency(current_spec, dep_spec, self.curr, edge_kwargs)
                    else:
                        self._attach_pending(root_spec, pending)
                        current_spec = dep_spec
                        pending = (dep_spec, self.curr, edge_kwargs)

            elif self.curr.lastgroup == _UNEXPECTED:
                self._raise_tokenization_error()

            else:
                # Any other token (e.g. a package name) starts the next spec in the input;
                # this spec is complete.
                break

        self._attach_pending(root_spec, pending)

        if self.curr is not None and self.curr is first_token:
            # Nothing was consumed, e.g. a stray ] in `zlib ]`: raise instead of looping forever
            self._raise_parsing_error("unexpected token")

        return root_spec

    def _rescan(self, pos: int) -> None:
        """Restart the scanner at ``pos`` in the input, the value of an unquoted when= condition"""
        self.scanner = FAST_SPEC_REGEX.scanner(self.literal_str, pos)  # type: ignore[attr-defined]
        self.curr = self.scanner.match()
        self.next = self.scanner.match()

    def _attach_pending(self, root_spec: "spack.spec.Spec", pending: Optional[tuple]) -> None:
        """Attach the pending ^ dependency, whose sub-dag is complete now."""
        if pending is not None:
            dep_spec, match, edge_kwargs = pending
            self._attach_dependency(root_spec, dep_spec, match, edge_kwargs)

    def _attach_dependency(
        self, target_spec: "spack.spec.Spec", dep_spec: "spack.spec.Spec", match, edge_kwargs: dict
    ) -> None:
        try:
            target_spec._add_dependency(dep_spec, **edge_kwargs)
        except spack.error.SpecError as e:
            raise SpecParsingError(str(e), match, self.literal_str) from e

    def _parse_node(
        self, initial_spec: Optional["spack.spec.Spec"] = None, initial_name: Optional[str] = None
    ) -> "spack.spec.Spec":
        """Parse a single spec node"""
        spec = initial_spec
        if spec is None:
            global Spec
            if Spec is None:
                from spack.spec import Spec as _Spec

                Spec = _Spec  # just `from spack.spec import Spec` is insufficient for mypy
            spec = Spec()

        # The lookahead is shifted in locals for speed and written back on return
        curr, next, scanner = self.curr, self.next, self.scanner

        # 1. Package name (or spec file). A missing name is fine: anonymous specs like
        # `@1.2 +debug` are valid.
        if initial_name:
            # Name came from a virtual assignment on the incoming edge, e.g. %c,cxx=gcc: only
            # node options can follow, a package name starts the next spec (`zlib %c=gcc gcc`)
            if "." in initial_name:
                spec.namespace, spec.name = initial_name.rsplit(".", 1)
            else:
                spec.name = initial_name
        elif curr:
            kind = curr.lastgroup
            value = curr.group(kind)
            if kind == _UNQUALIFIED_PACKAGE_NAME:
                if value != "*":  # `*` is an anonymous node, as in `%*+shared`
                    spec.name = value
                curr = next
                next = scanner.match() if curr is not None else None
            elif kind == _FULLY_QUALIFIED_PACKAGE_NAME:
                spec.namespace, spec.name = value.rsplit(".", 1)
                curr = next
                next = scanner.match() if curr is not None else None
            elif kind == _FILENAME:
                # A spec file is a complete node: read it and return
                if not os.path.exists(value):
                    raise spack.error.NoSuchSpecFileError(f"No such spec file: '{value}'")
                spec._dup(spack.spec.Spec.from_specfile(value))
                self.curr, self.next = next, scanner.match()
                return spec
            elif kind == _UNEXPECTED:
                self._raise_tokenization_error()
            # else: no name; fall through to attributes of an anonymous node

        # 2. Node attributes: version, variants, flags, and abstract hash, in any order
        has_version = False
        while curr:
            kind = curr.lastgroup

            if kind == _VERSION:
                if has_version:
                    self.curr = curr
                    self._raise_parsing_error("Spec cannot have multiple versions")

                try:
                    if curr.group(_GIT_VERSION):
                        spec.versions = spack.version.VersionList(
                            [spack.version.GitVersion(curr.group(_GIT_VERSION))]
                        )
                        spec.attach_git_version_lookup()
                    else:
                        spec.versions = spack.version.VersionList(curr.group(_VERSION_LIST))
                except ValueError as e:
                    # The tokenizer accepts more than VersionList does, e.g. @=1:2
                    self.curr = curr
                    self._raise_parsing_error(str(e))
                has_version = True

            elif kind == _BOOL_VARIANT:
                prefix = curr.group(_BV_PREFIX)
                name = curr.group(_BV_NAME)
                propagate = len(prefix) == 2
                value = prefix.startswith("+")
                try:
                    spec._add_flag(name, value, propagate, concrete=True)
                except Exception as e:
                    self.curr = curr
                    self._raise_parsing_error(str(e))

            elif kind == _KEY_VALUE_PAIR:
                name = curr.group(_KV_NAME)
                sep = curr.group(_KV_SEP)
                value = curr.group(_KV_VALUE)
                propagate = "==" in sep
                concrete = sep.startswith(":")
                try:
                    spec._add_flag(name, strip_quotes(value), propagate, concrete)
                except Exception as e:
                    self.curr = curr
                    self._raise_parsing_error(str(e))

            elif kind == _DAG_HASH:
                if spec.abstract_hash:
                    # A second hash belongs to the next spec, e.g. `spack find /abc /def`
                    break
                spec.abstract_hash = curr.group().strip()[1:]

            else:
                # DEPENDENCY, END_EDGE_PROPERTIES, a package name, or UNEXPECTED: this node
                # is done; the caller decides what is valid next.
                break

            # Accept the token
            curr = next
            next = scanner.match() if curr is not None else None

        self.curr, self.next = curr, next
        return spec

    def all_specs(self) -> List["spack.spec.Spec"]:
        """Return all the specs that remain to be parsed"""
        return list(iter(self.next_spec, None))
