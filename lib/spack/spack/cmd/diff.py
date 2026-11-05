# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import argparse
import contextlib
import os
import shutil
import sys
import tempfile
from typing import Dict, List, Optional, Tuple

import spack.cmd
import spack.config
import spack.enums
import spack.environment as ev
import spack.environment.environment
import spack.error
import spack.hash_lookup
import spack.repo
import spack.spec
import spack.spec_diff
import spack.util.spack_json as sjson
import spack.variant
from spack.active_environment import active_environment
from spack.environment import diff as env_diff_core
from spack.solver import asp, clauses
from spack.util import tty
from spack.util.tty.colify import render_blocks, terminal_columns
from spack.util.tty.color import cescape, clen, colorize, cprint, get_color_when

description = "compare two concrete environments, or two specs"
section = "query"
level = "long"


def setup_parser(subparser: argparse.ArgumentParser) -> None:
    subparser.add_argument(
        "-s",
        "--specs",
        action="store_true",
        default=False,
        dest="compare_specs",
        help="compare two specs instead of two environments",
    )
    subparser.add_argument(
        "--json",
        action="store_true",
        default=False,
        dest="dump_json",
        help="dump json output instead of pretty printing",
    )
    subparser.add_argument(
        "--no-prune",
        action="store_false",
        default=True,
        dest="prune",
        help="report every differing node, instead of reporting the node where a difference "
        "first appears and skipping the subgraph below it",
    )
    subparser.add_argument(
        "--first",
        action="store_true",
        default=False,
        dest="load_first",
        help="load the first match if multiple packages match the spec",
    )
    subparser.add_argument(
        "-a",
        "--attribute",
        action="append",
        help="select the attributes to show (defaults to all)",
    )
    subparser.add_argument(
        "--ignore", action="append", help="omit diffs related to these dependencies"
    )
    subparser.add_argument(
        "inputs",
        nargs=argparse.REMAINDER,
        metavar="before after",
        help="two concrete environments, each a name, a directory, or a lockfile; the second is "
        "taken to be the later state of the first. With --specs, two specs",
    )


def diff(parser, args):
    if args.compare_specs:
        _diff_specs(args)
    else:
        _diff_environments(args)


#: Above this many input specs reaching the same divergent node, report a count instead of a list
_MAX_LISTED_INPUTS = 3

#: Indentation of every section header and of the entries under it
_BAND_INDENT = 2

#: Width assumed for section headers when the output is not going to a terminal
_DEFAULT_WIDTH = 80

#: Categories with no spec syntax to be rendered in, reported on a line of their own instead
_ANNOTATED_CATEGORIES = (spack.spec_diff.DiffCategory.EXTERNAL, spack.spec_diff.DiffCategory.OTHER)


def _is_lockfile(path: str) -> bool:
    """Whether a file is a Spack lockfile, decided by its content rather than by its name."""
    try:
        with open(path, "r", encoding="utf-8") as stream:
            data = sjson.load(stream)
    except (OSError, ValueError):
        return False
    meta = data.get("_meta") if isinstance(data, dict) else None
    return isinstance(meta, dict) and meta.get("file-type") == "spack-lockfile"


def _open_environment_to_diff(
    stack: contextlib.ExitStack, argument: str
) -> Tuple[ev.Environment, Dict[str, Optional[str]]]:
    """Resolve one command-line argument to an environment, and to the identity to report for it.

    A name or an environment directory is opened where it is. A lockfile is materialized as a
    throwaway environment, which is deleted when the stack is closed, so that comparing two
    lockfiles does not require creating an environment for each of them first.

    Raises:
        spack.environment.environment.SpackEnvironmentError: if the argument is not an
            environment, or is a file that is not a lockfile
    """
    path = spack.config.substitute_path_variables(argument)
    if os.path.isfile(path):
        root = stack.enter_context(tempfile.TemporaryDirectory(prefix="spack-env-diff-"))
        # create_in_dir tells a lockfile from a manifest by suffix
        init_file = path
        if not path.endswith((".lock", ".json")):
            init_file = os.path.join(root, ev.lockfile_name)
            shutil.copy(path, init_file)
        try:
            env = ev.create_in_dir(os.path.join(root, "env"), init_file=init_file)
        except ev.SpackEnvironmentError as e:
            # Parse the file only on failure, to word the error
            if _is_lockfile(path):
                raise
            hint = f"pass an environment name, a directory, or a '{ev.lockfile_name}' file"
            if os.path.basename(path) == ev.manifest_name:
                directory = os.path.dirname(argument) or "."
                hint = f"to compare the environment it describes, pass '{directory}'"
            raise ev.SpackEnvironmentError(f"'{argument}' is not a Spack lockfile", hint) from e
        # Report the lockfile, not the temporary directory, as this side's identity
        return env, {"name": None, "path": os.path.abspath(path)}

    if not ev.is_env_dir(path) and not ev.exists(argument):
        raise ev.SpackEnvironmentError(
            f"no environment, environment directory, or lockfile named '{argument}'",
            "to compare two specs, use `spack diff --specs`",
        )
    env = ev.environment_from_name_or_dir(argument)
    return env, {"name": env.name, "path": env.path}


def _diff_environments(args) -> None:
    if len(args.inputs) != 2:
        args.subparser.error("you must provide two environments to compare")
    before, after = args.inputs

    with contextlib.ExitStack() as stack:
        env_before, identity_before = _open_environment_to_diff(stack, before)
        env_after, identity_after = _open_environment_to_diff(stack, after)

        result = env_diff_core.diff_environments(
            env_before, env_after, prune=args.prune, label_a=before, label_b=after
        )

        if args.dump_json:
            # Keys stay positional: only the pretty output assumes a direction
            identities = {"a": identity_before, "b": identity_after}
            print(sjson.dumps({**result.as_dict(), "environments": identities}))
            return

        EnvironmentDiffRenderer(result, before, after).render()


def shift(asp_function: asp.AspFunction) -> asp.AspFunction:
    """Transforms ``attr("foo", "bar")`` into ``foo("bar")``."""
    args = asp_function.args
    if not args:
        raise ValueError(f"Can't shift ASP function with no arguments: {str(asp_function)}")
    return asp.AspFunction(args[0], args[1:])


def compare_specs(a, b, to_string=False, color=None, ignore_packages=None):
    """
    Generate a comparison, including diffs (for each side) and an intersection.

    We can either print the result to the console, or parse
    into a json object for the user to save. We return an object that shows
    the differences, intersection, and names for a pair of specs a and b.

    Arguments:
        a (spack.spec.Spec): the first spec to compare
        b (spack.spec.Spec): the second spec to compare
        a_name (str): the name of spec a
        b_name (str): the name of spec b
        to_string (bool): return an object that can be json dumped
        color (bool): whether to format the names for the console
    """
    if color is None:
        color = get_color_when()

    a = a.copy()
    b = b.copy()

    if ignore_packages:
        for pkg_name in ignore_packages:
            a.trim(pkg_name)
            b.trim(pkg_name)

    # Prepare a clause generator to parse differences
    generator = clauses.SpecClauseGenerator(repo=spack.repo.PATH)

    # get facts for specs, making sure to include build dependencies of concrete
    # specs and to descend into dependency hashes so we include all facts.
    a_facts = {
        shift(func)
        for func in generator.spec_clauses(
            a, body=True, expand_hashes=True, concrete_build_deps=True, include_runtimes=True
        )
        if func.name == "attr"
    }
    b_facts = {
        shift(func)
        for func in generator.spec_clauses(
            b, body=True, expand_hashes=True, concrete_build_deps=True, include_runtimes=True
        )
        if func.name == "attr"
    }

    # We want to present them to the user as simple key: values
    intersect = sorted(a_facts.intersection(b_facts))
    spec1_not_spec2 = sorted(a_facts.difference(b_facts))
    spec2_not_spec1 = sorted(b_facts.difference(a_facts))

    # Format the spec names to be colored
    fmt = "{name}{@version}{/hash}"
    a_name = a.format(fmt, color=color)
    b_name = b.format(fmt, color=color)

    # We want to show what is the same, and then difference for each
    return {
        "intersect": flatten(intersect) if to_string else intersect,
        "a_not_b": flatten(spec1_not_spec2) if to_string else spec1_not_spec2,
        "b_not_a": flatten(spec2_not_spec1) if to_string else spec2_not_spec1,
        "a_name": a_name,
        "b_name": b_name,
    }


def flatten(functions):
    """
    Given a list of ASP functions, convert into a list of key: value tuples.

    We are squashing whatever is after the first index into one string for
    easier parsing in the interface
    """
    updated = []
    for fun in functions:
        updated.append([fun.name, " ".join(str(a) for a in fun.args)])
    return updated


def print_difference(c, attributes="all", out=None):
    """
    Print the difference.

    Given a diffset for A and a diffset for B, print red/green diffs to show
    the differences.
    """
    # Default to standard out unless another stream is provided
    out = out or sys.stdout

    A = c["b_not_a"]
    B = c["a_not_b"]

    cprint("@R{--- %s}" % c["a_name"])  # bright red
    cprint("@G{+++ %s}" % c["b_name"])  # bright green

    # Cut out early if we don't have any differences!
    if not A and not B:
        print("No differences\n")
        return

    def group_by_type(diffset):
        grouped = {}
        for entry in diffset:
            if entry[0] not in grouped:
                grouped[entry[0]] = []
            grouped[entry[0]].append(entry[1])

        # Sort by second value to make comparison slightly closer
        for key, values in grouped.items():
            values.sort()
        return grouped

    A = group_by_type(A)
    B = group_by_type(B)

    # print a directionally relevant diff
    keys = list(A) + list(B)

    category = None
    for key in keys:
        if "all" not in attributes and key not in attributes:
            continue

        # Write the attribute, B is subtraction A is addition
        subtraction = [] if key not in B else B[key]
        addition = [] if key not in A else A[key]

        # Bail out early if we don't have any entries
        if not subtraction and not addition:
            continue

        # If we have a new category, create a new section
        if category != key:
            category = key

            # print category in bold, colorized
            cprint("@*b{@@ %s @@}" % category)  # bold blue

        # Print subtractions first
        while subtraction:
            cprint("@R{-  %s}" % subtraction.pop(0))  # bright red
            if addition:
                cprint("@G{+  %s}" % addition.pop(0))  # bright green

        # Any additions left?
        while addition:
            cprint("@G{+  %s}" % addition.pop(0))


def _diff_specs(args) -> None:
    env = active_environment()

    if len(args.inputs) != 2:
        args.subparser.error("you must provide two specs to diff")

    specs = []
    for spec in spack.cmd.parse_specs(args.inputs):
        # If the spec has a hash, check it before disambiguating
        spack.hash_lookup.replace_hash(spec)
        if spec.concrete:
            specs.append(spec)
        else:
            specs.append(spack.cmd.disambiguate_spec(spec, env, first=args.load_first))

    # Calculate the comparison (c)
    color = False if args.dump_json else get_color_when()
    c = compare_specs(specs[0], specs[1], to_string=True, color=color, ignore_packages=args.ignore)

    # Default to all attributes
    attributes = args.attribute or ["all"]

    if args.dump_json:
        print(sjson.dumps(c))
    else:
        tty.warn("This interface is subject to change.\n")
        print_difference(c, attributes)


def _variant_default(node: spack.spec.Spec, key: str) -> Optional[spack.variant.VariantValue]:
    """Returns the default value of a variant for a node, or None if it cannot be determined.

    An environment can have been concretized against a package repository that no longer contains
    this package, or no longer defines this variant, so the lookup is allowed to come up empty.
    """
    try:
        # get_variant picks the definition whose `when` the node satisfies
        return node.package.get_variant(key).make_default()
    except (spack.error.SpackError, ValueError):
        return None


def _attribute_style(
    divergence: spack.spec_diff.NodeDivergence, attribute: spack.spec_diff.AttributeDiff
) -> spack.enums.PartStyle:
    """Returns how prominently one difference of a divergent node should be rendered.

    A difference that is what one would expect from a re-concretization is rendered normally, and
    a suspicious one is highlighted, taking the second environment to be the later state of the
    first. Only versions and variants have an expected direction, so any other difference is
    highlighted.
    """
    if attribute.category is spack.spec_diff.DiffCategory.VERSION:
        try:
            newer = divergence.node_b.version > divergence.node_a.version
        except TypeError:  # two versions that cannot be ordered say nothing about direction
            newer = False
        return spack.enums.PartStyle.NORMAL if newer else spack.enums.PartStyle.HIGHLIGHT

    if attribute.category is spack.spec_diff.DiffCategory.VARIANT:
        # Judge the value on the second side, or on the first if the variant was dropped
        node = divergence.node_b
        if attribute.key not in node.variants:
            node = divergence.node_a
        value = node.variants[attribute.key]
        default = _variant_default(node, attribute.key)
        if default is not None and set(value.values) == set(default.values):
            return spack.enums.PartStyle.NORMAL
        return spack.enums.PartStyle.HIGHLIGHT

    return spack.enums.PartStyle.HIGHLIGHT


#: How prominently each differing (category, key) of a node should be rendered
_StyleMap = Dict[Tuple[spack.spec_diff.DiffCategory, str], spack.enums.PartStyle]


def _node_styles(divergence: spack.spec_diff.NodeDivergence) -> _StyleMap:
    """Judge every difference of a node once, so both sides can be rendered from one pass."""
    return {
        (attribute.category, attribute.key): _attribute_style(divergence, attribute)
        for attribute in divergence.attributes
    }


def _format_divergent_node(
    divergence: spack.spec_diff.NodeDivergence, *, first: bool, styles: _StyleMap
) -> str:
    """Render one side of a divergent node as an abstract spec holding only the differences.

    Every part that is equal on both sides is hidden, so the result is a valid abstract spec
    naming exactly what changed on that node.

    Args:
        divergence: the node where the two DAGs diverge
        first: render the node from the first environment, otherwise the one from the second
        styles: styles from :func:`_node_styles`, shared by the two sides of the node
    """
    categories = {attribute.category for attribute in divergence.attributes}
    node = divergence.node_a if first else divergence.node_b

    def style(category: spack.spec_diff.DiffCategory, key: str = "") -> spack.enums.PartStyle:
        return styles.get((category, key), spack.enums.PartStyle.HIDDEN)

    # Flags and namespace have no style callback, so all flags show when any differs
    format_string = "{name}{@version}"
    if spack.spec_diff.DiffCategory.FLAGS in categories:
        format_string += "{compiler_flags}"
    format_string += "{variants}"
    if spack.spec_diff.DiffCategory.NAMESPACE in categories:
        format_string += "{ namespace=namespace}"
    # The hash goes before the dependency sigils appended below, or it would bind to one
    format_string += (
        "{ platform=architecture.platform}{ os=architecture.os}{ target=architecture.target}"
        "{/hash:7}"
    )

    rendered = node.format(
        format_string,
        color=None,
        version_style_fn=lambda n: style(spack.spec_diff.DiffCategory.VERSION),
        variant_style_fn=lambda n, key: style(spack.spec_diff.DiffCategory.VARIANT, key),
        architecture_style_fn=lambda n, part: style(
            spack.spec_diff.DiffCategory.ARCHITECTURE, part
        ),
    )

    # Dependencies are edges, not part of the node format string
    edges = []
    for attribute in divergence.attributes:
        if attribute.category is not spack.spec_diff.DiffCategory.DEPENDENCY:
            continue
        own = attribute.value_a if first else attribute.value_b
        if not own:
            continue  # the edge only exists on the other side
        other = attribute.value_b if first else attribute.value_a
        # On both sides only the edge differs, so show its attributes
        edges.append(f"%[{own}]{attribute.key}" if other else f"%{attribute.key}")

    if edges:
        rendered += " " + colorize("@_R{%s}" % cescape(" ".join(edges)))

    return rendered


#: A divergence and the input specs that reach it
_Entry = Tuple[spack.spec_diff.NodeDivergence, List[ev.UserSpecId]]


def _format_root(root: ev.UserSpecId, *, with_group: bool = True) -> str:
    """Render an input spec, naming its group only when it is not the default one."""
    if not with_group or root.group == spack.environment.environment.DEFAULT_USER_SPEC_GROUP:
        return str(root.spec)
    return f"{root.spec} (group: {root.group})"


def _is_recipe_change(node: spack.spec_diff.NodeDivergence) -> bool:
    """Whether a divergence reports a changed recipe rather than a configuration difference."""
    return any(
        attribute.category is spack.spec_diff.DiffCategory.RECIPE for attribute in node.attributes
    )


def _annotations(node: spack.spec_diff.NodeDivergence) -> List[str]:
    """Render the differences that a spec literal has no room for, one per line.

    The prefix of an external, and the node state the catch-all reports, have no spec syntax to be
    written in. Putting them on their own line keeps the two rendered specs above parseable.
    """
    lines = []
    for attribute in node.attributes:
        if attribute.category not in _ANNOTATED_CATEGORIES:
            continue
        key = f" {attribute.key}" if attribute.key else ""
        lines.append(
            colorize(
                f"    {attribute.category.value}{key}: "
                f"@R{{{cescape(attribute.value_a or '(none)')}}} -> "
                f"@G{{{cescape(attribute.value_b or '(none)')}}}"
            )
        )
    return lines


def _group_divergences(
    divergences: List[env_diff_core.UserSpecDivergence],
) -> Tuple[Dict[str, List[_Entry]], List[_Entry]]:
    """Split divergences into configuration differences per group, and recipe changes.

    A single divergence is typically reached from many input specs, and reporting it once per
    input spec makes the output grow with the size of the environment rather than with the number
    of differences. Findings are therefore reported once, against the input specs reaching them.

    Configuration differences are keyed by node, within the group of the input spec reaching them,
    since a group exists precisely to build the same specs under a different configuration. Recipe
    changes are instead a property of a package file: they span groups, and are keyed by package.
    Keying those by node, or even by package hash, would repeat one fact once per instance, since
    a package hash is taken over the canonical source *filtered for its own spec*, so a single
    edit to a package file yields a different pair of package hashes for every differently
    configured instance of it.
    """
    config: Dict[str, Dict[Tuple[str, str], _Entry]] = {}  # group -> (hash of a, hash of b)
    recipes: Dict[Tuple[str, str], _Entry] = {}  # (namespace, name)

    for input_divergence in divergences:
        root = input_divergence.root
        for node in input_divergence.nodes:
            if _is_recipe_change(node):
                key = (node.node_a.namespace or "", node.node_a.name)
                recipes.setdefault(key, (node, []))[1].append(root)
            else:
                node_key = (node.node_a.dag_hash(), node.node_b.dag_hash())
                config.setdefault(root.group, {}).setdefault(node_key, (node, []))[1].append(root)

    # Default group first, as in concretization; entries ordered by node
    default = spack.environment.environment.DEFAULT_USER_SPEC_GROUP
    by_group = {
        group: [
            (node, env_diff_core.sorted_roots(roots))
            for node, roots in sorted(
                config[group].values(), key=lambda x: spack.spec_diff.node_sort_key(x[0])
            )
        ]
        for group in sorted(config, key=lambda x: (x != default, x))
    }

    return by_group, [
        (recipes[key][0], env_diff_core.sorted_roots(recipes[key][1])) for key in sorted(recipes)
    ]


def _reached_from(roots: List[ev.UserSpecId], *, with_group: bool = True) -> str:
    """Describe which input specs reach a divergent node, without listing an unbounded number."""
    if len(roots) > _MAX_LISTED_INPUTS:
        return f"from {len(roots)} input specs"
    return "from " + ", ".join(_format_root(root, with_group=with_group) for root in roots)


class EnvironmentDiffRenderer:
    """Renders an ``EnvironmentDiff`` to the terminal, for the two named environments."""

    def __init__(
        self, result: env_diff_core.EnvironmentDiff, name_before: str, name_after: str
    ) -> None:
        self.result = result
        self.name_before = name_before
        self.name_after = name_after
        # Environment names can be long paths, so they are printed once and labels used after
        self.label_before = colorize("@R{before}")
        self.label_after = colorize("@G{after}")
        # Tags are padded so the two sides align; labels stay unpadded for section headers
        self.tag_before = f"{self.label_before}: "
        self.tag_after = f"{self.label_after}:  "
        # Zero when the output is not a terminal, which keeps the blocks in a single column
        self.columns = terminal_columns()

    def _section(self, label: str, blocks: List[List[str]]) -> None:
        """Print a section header followed by its blocks.

        The header spans its own content rather than the console, so that a short section does not
        get a rule running off to the right.
        """
        lines = render_blocks(blocks, self.columns, indent=_BAND_INDENT)
        content = max((clen(line) for line in lines), default=0)
        width = min(content, self.columns or _DEFAULT_WIDTH)
        print(tty.band(colorize(label), width, indent=_BAND_INDENT))
        for line in lines:
            print(line)
        print()

    def _node_block(
        self, node: spack.spec_diff.NodeDivergence, roots: List[ev.UserSpecId]
    ) -> List[str]:
        """Render one divergent node as a block: a header, the two sides, then its annotations."""
        styles = _node_styles(node)
        return [
            f"{node.node_a.name}  ({_reached_from(roots, with_group=False)})",
            f"    {self.tag_before}{_format_divergent_node(node, first=True, styles=styles)}",
            f"    {self.tag_after}{_format_divergent_node(node, first=False, styles=styles)}",
        ] + _annotations(node)

    def render(self) -> None:
        print()
        print(f"{' ' * _BAND_INDENT}{self.tag_before}{self.name_before}")
        print(f"{' ' * _BAND_INDENT}{self.tag_after}{self.name_after}")
        print()

        result = self.result
        if result.equivalent:
            print(f"{' ' * _BAND_INDENT}the two environments are equivalent")
            print()
            return

        sides = (
            (self.label_before, result.inputs.only_in_a),
            (self.label_after, result.inputs.only_in_b),
        )
        for label, only in sides:
            if only:
                self._section(
                    f"@*{{Input specs only in}} {label}",
                    [[_format_root(root)] for root in env_diff_core.sorted_roots(only)],
                )

        config_by_group, recipes = _group_divergences(result.divergences)

        # Only name groups when there is more than the default one
        default = spack.environment.environment.DEFAULT_USER_SPEC_GROUP
        show_groups = list(config_by_group) != [default]

        for group, entries in config_by_group.items():
            self._section(
                f"@*{{Group: {cescape(group)}}}" if show_groups else "@*{Node differences}",
                [self._node_block(node, roots) for node, roots in entries],
            )

        # Recipe changes come last, as the least actionable finding
        if recipes:
            self._section(
                "@*{Packages whose recipe differs}",
                [[f"{node.node_a.name}  ({_reached_from(roots)})"] for node, roots in recipes],
            )

        if result.unresolved:
            self._section(
                "@*{Common input specs with no difference to point at}",
                [[_format_root(r)] for r in env_diff_core.sorted_roots(result.unresolved)],
            )
