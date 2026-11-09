# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import argparse
from typing import Dict, List, Optional, Tuple

import spack.cmd
import spack.enums
import spack.environment as ev
import spack.error
import spack.hash_lookup
import spack.spec
import spack.spec_diff
import spack.store
import spack.util.spack_json as sjson
import spack.variant
from spack.active_environment import active_environment
from spack.cmd.common import arguments
from spack.util import tty
from spack.util.lang import stable_partition
from spack.util.tty.colify import render_blocks, terminal_columns
from spack.util.tty.color import cescape, clen, colorize

description = "compare two specs"
section = "query"
level = "long"


def setup_parser(subparser: argparse.ArgumentParser) -> None:
    arguments.add_common_arguments(subparser, ["specs"])
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


def diff(parser, args) -> None:
    _diff_specs(args)


#: Indentation of every section header and of the entries under it
_BAND_INDENT = 2

#: Width assumed for section headers when the output is not going to a terminal
_DEFAULT_WIDTH = 80

#: Categories with no spec syntax to be rendered in, reported on a line of their own instead
_ANNOTATED_CATEGORIES = (spack.spec_diff.DiffCategory.EXTERNAL, spack.spec_diff.DiffCategory.OTHER)


def _concrete_spec(spec: spack.spec.Spec, env: Optional[ev.Environment]) -> spack.spec.Spec:
    """Resolve a spec argument to the single concrete spec it matches."""
    # If the spec has a hash, check it before disambiguating
    spack.hash_lookup.replace_hash(spec)
    if spec.concrete:
        return spec
    # In an environment, its concrete specs whether installed or not
    matches = env.all_matching_specs(spec) if env else spack.store.STORE.db.query(spec)
    if not matches:
        where = f"concrete specs of environment '{env.name}'" if env else "installed packages"
        raise spack.error.SpackError(f"Spec '{spec}' matches no {where}.")
    spack.cmd.ensure_single_spec_or_die(spec, matches)
    return matches[0]


def _diff_specs(args) -> None:
    """Compare two concrete specs."""
    specs = spack.cmd.parse_specs(args.specs)
    if len(specs) != 2:
        args.subparser.error("you must provide two specs to compare")

    env = active_environment()
    before, after = (_concrete_spec(spec, env) for spec in specs)
    result = spack.spec_diff.diff_specs(before, after, prune=args.prune)

    if args.dump_json:
        identities = {
            "a": {"name": before.name, "hash": before.dag_hash()},
            "b": {"name": after.name, "hash": after.dag_hash()},
        }
        print(sjson.dumps({**result.as_dict(), "specs": identities}))
    else:
        name_format = "{name}{@version}{/hash:7}"
        SpecDiffRenderer(result, before.cformat(name_format), after.cformat(name_format)).render()


def _variant_default(node: spack.spec.Spec, key: str) -> Optional[spack.variant.VariantValue]:
    try:
        # get_variant picks the definition whose `when` the node satisfies
        return node.package.get_variant(key).make_default()
    except (spack.error.SpackError, ValueError):
        # The current repository may no longer have the package, or the variant
        return None


def _attribute_style(
    divergence: spack.spec_diff.NodeDivergence, attribute: spack.spec_diff.AttributeDiff
) -> spack.enums.PartStyle:
    """Returns HIGHLIGHT for a difference unexpected when re-concretizing the first side into the
    second, and NORMAL otherwise."""
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

    # Only versions and variants have an expected direction
    return spack.enums.PartStyle.HIGHLIGHT


#: How prominently each differing (category, key) of a node should be rendered
_StyleMap = Dict[Tuple[spack.spec_diff.DiffCategory, str], spack.enums.PartStyle]


def _node_styles(divergence: spack.spec_diff.NodeDivergence) -> _StyleMap:
    return {
        (attribute.category, attribute.key): _attribute_style(divergence, attribute)
        for attribute in divergence.attributes
    }


def _format_divergent_node(
    divergence: spack.spec_diff.NodeDivergence, *, first: bool, styles: _StyleMap
) -> str:
    """Render one side of a divergent node as an abstract spec holding only the differences."""
    categories = {attribute.category for attribute in divergence.attributes}
    node = divergence.node_a if first else divergence.node_b

    # A part equal on both sides has no style, and is hidden
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


def _recipe_key(node: spack.spec_diff.NodeDivergence) -> Tuple[str, str]:
    """Key of a recipe change: one per package, since every instance has its own package hash."""
    return node.node_a.namespace or "", node.node_a.name


def _is_recipe_change(node: spack.spec_diff.NodeDivergence) -> bool:
    return any(
        attribute.category is spack.spec_diff.DiffCategory.RECIPE for attribute in node.attributes
    )


def _annotations(node: spack.spec_diff.NodeDivergence) -> List[str]:
    """Render the differences that a spec literal has no room for, one per line."""
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


class _DiffRenderer:
    """Layout of the output of ``spack diff``."""

    def __init__(self, name_before: str, name_after: str) -> None:
        self.name_before = name_before
        self.name_after = name_after
        # Names can be long paths, so they are printed once and labels used after
        self.label_before = colorize("@R{before}")
        self.label_after = colorize("@G{after}")
        # Tags are padded so the two sides align; labels stay unpadded for section headers
        self.tag_before = f"{self.label_before}: "
        self.tag_after = f"{self.label_after}:  "
        # Zero when the output is not a terminal, which keeps the blocks in a single column
        self.columns = terminal_columns()

    def _line(self, text: str) -> None:
        print(f"{' ' * _BAND_INDENT}{text}")

    def _names(self) -> None:
        """Print what is compared, once, so that sections can refer to the two sides by label."""
        print()
        self._line(f"{self.tag_before}{self.name_before}")
        self._line(f"{self.tag_after}{self.name_after}")
        print()

    def _section(self, label: str, blocks: List[List[str]]) -> None:
        lines = render_blocks(blocks, self.columns, indent=_BAND_INDENT)
        # The rule spans the content rather than the console, so a short section gets a short one
        content = max((clen(line) for line in lines), default=0)
        width = min(content, self.columns or _DEFAULT_WIDTH)
        print(tty.band(colorize(label), width, indent=_BAND_INDENT))
        for line in lines:
            print(line)
        print()

    def _node_block(self, node: spack.spec_diff.NodeDivergence, header: str) -> List[str]:
        styles = _node_styles(node)
        return [
            header,
            f"    {self.tag_before}{_format_divergent_node(node, first=True, styles=styles)}",
            f"    {self.tag_after}{_format_divergent_node(node, first=False, styles=styles)}",
        ] + _annotations(node)


class SpecDiffRenderer(_DiffRenderer):
    """Renders a ``SpecDiff`` to the terminal, for the two named specs."""

    def __init__(
        self, result: spack.spec_diff.SpecDiff, name_before: str, name_after: str
    ) -> None:
        super().__init__(name_before, name_after)
        self.result = result

    def render(self) -> None:
        self._names()

        result = self.result
        if result.equivalent:
            self._line("the two specs are identical")
            print()
            return

        nodes = sorted(result.nodes, key=spack.spec_diff.node_sort_key)
        recipe_changes, config = stable_partition(nodes, _is_recipe_change)
        if config:
            self._section(
                "@*{Node differences}",
                [self._node_block(node, node.node_a.name) for node in config],
            )

        recipes = {_recipe_key(node) for node in recipe_changes}
        if recipes:
            self._section(
                "@*{Packages whose recipe differs}", [[name] for _, name in sorted(recipes)]
            )

        if not nodes:
            self._line("the two specs differ, with no difference to point at")
            print()
