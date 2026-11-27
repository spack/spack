# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import argparse
import contextlib
import os
import shutil
import tempfile
from typing import IO, Any, Callable, Dict, List, NamedTuple, Optional, Tuple

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
import spack.store
import spack.util.spack_json as sjson
import spack.util.spack_yaml as syaml
import spack.variant
from spack.active_environment import active_environment
from spack.environment import diff as env_diff_core
from spack.util import tty
from spack.util.lang import stable_partition
from spack.util.tty.colify import render_blocks, terminal_columns
from spack.util.tty.color import cescape, clen, colorize

description = "compare two concrete environments, or two specs"
section = "query"
level = "long"

#: Exit status of ``spack diff --exit-code`` when the two inputs differ
EXIT_DIFFERENT = 4


def setup_parser(subparser: argparse.ArgumentParser) -> None:
    json = subparser.add_argument(
        "--json",
        action="store_true",
        default=False,
        dest="dump_json",
        help="dump json output instead of pretty printing",
    )
    no_prune = subparser.add_argument(
        "--no-prune",
        action="store_false",
        default=True,
        dest="prune",
        help="report every differing node, instead of reporting the node where a difference "
        "first appears and skipping the subgraph below it",
    )
    exit_code = subparser.add_argument(
        "--exit-code",
        action="store_true",
        default=False,
        help=f"exit with status {EXIT_DIFFERENT} if the two inputs differ, and 0 otherwise",
    )
    subparser.add_argument(
        "inputs",
        nargs=argparse.REMAINDER,
        metavar="before after",
        help="two concrete environments, each a name, a directory, or a lockfile, or else two "
        "specs, each a spec file, a hash, or a spec matching one spec of the active environment "
        "or else one installed spec; the second is taken to be the later state of the first",
    )
    # The inputs take the rest of the command line, so options written after them end up there
    subparser.set_defaults(
        option_strings={"-h", "--help"}.union(
            *(x.option_strings for x in (json, no_prune, exit_code))
        )
    )


def diff(parser, args) -> int:
    # REMAINDER keeps a leading `--`
    if args.inputs[:1] == ["--"]:
        args.inputs = args.inputs[1:]
    misplaced = [x for x in args.inputs if x in args.option_strings]
    if misplaced:
        args.subparser.error(
            f"options must come before the two environments or specs: {', '.join(misplaced)}"
        )

    with contextlib.ExitStack() as stack:
        resolved = _resolve_inputs(stack, args.inputs)
        environments = [x.environment for x in resolved if x.environment is not None]
        if len(environments) == 2:
            equivalent = _diff_environments(args, *environments)
        else:
            equivalent = _diff_specs(args, resolved)
    return EXIT_DIFFERENT if args.exit_code and not equivalent else 0


#: Above this many input specs reaching the same divergent node, report a count instead of a list
_MAX_LISTED_INPUTS = 3

#: Indentation of every section header and of the entries under it
_BAND_INDENT = 2

#: Width assumed for section headers when the output is not going to a terminal
_DEFAULT_WIDTH = 80

#: How the two packages providing a common virtual input are rendered
_PROVIDER_FORMAT = "{name}{@version}{variants}{/hash:7}"

#: Categories with no spec syntax to be rendered in, reported on a line of their own instead
_ANNOTATED_CATEGORIES = (spack.spec_diff.DiffCategory.EXTERNAL, spack.spec_diff.DiffCategory.OTHER)


def _load_mapping(path: str, load: Callable[[IO[str]], Any]) -> Dict[str, Any]:
    try:
        with open(path, "r", encoding="utf-8") as stream:
            data = load(stream)
    except (OSError, ValueError, spack.error.SpackError):
        return {}
    return data if isinstance(data, dict) else {}


def _load_input_file(path: str) -> Dict[str, Any]:
    """The mapping a lockfile or a spec file holds, or an empty one for any other file."""
    data = _load_mapping(path, sjson.load)
    # Lockfiles are always JSON, spec files are JSON or YAML
    if not data and not path.endswith(".json"):
        data = _load_mapping(path, syaml.load)
    return data


def _is_lockfile(data: Dict[str, Any]) -> bool:
    meta = data.get("_meta")
    return isinstance(meta, dict) and meta.get("file-type") == "spack-lockfile"


def _is_specfile(data: Dict[str, Any]) -> bool:
    return isinstance(data.get("spec"), dict)


#: Extensions of the files an argument can name: lockfiles, manifests and spec files
_FILE_EXTENSIONS = (".lock", ".json", ".yaml", ".yml")


#: An environment to compare, and how the JSON output identifies it
_EnvironmentInput = Tuple[ev.Environment, Dict[str, Optional[str]]]


class _Input(NamedTuple):
    """One of two arguments of ``spack diff``, resolved to an environment or to a spec. The
    environment and the spec are both None for an argument that is not a spec on its own, like
    ``+mpi``."""

    #: The environment the argument refers to
    environment: Optional[_EnvironmentInput] = None
    #: The spec the argument is on its own, read from a spec file or parsed
    spec: Optional[spack.spec.Spec] = None
    #: Why a word that also names a path is not an environment
    path_error: Optional[ev.SpackEnvironmentError] = None


def _is_word(argument: str) -> bool:
    """Whether an argument is a bare word, such as a package name. A word is never refused as a
    path, so that a file or a directory in the working directory does not hide a package."""
    return bool(spack.environment.environment.valid_env_name(argument)) and os.sep not in argument


def _looks_like_path(argument: str, path: str) -> bool:
    # Substitution expands `~/x` or `$HOME`, and leaves spec syntax like `~shared` alone
    return os.sep in argument or argument.startswith(".") or path != argument


def _standalone_spec(argument: str) -> Optional[spack.spec.Spec]:
    """The spec an argument is on its own, if it is one spec with a name or a hash."""
    try:
        specs = spack.cmd.parse_specs([argument])
    except (spack.error.SpecSyntaxError, spack.error.SpecError):
        return None
    if len(specs) != 1 or not (specs[0].name or specs[0].abstract_hash):
        return None
    return specs[0]


def _not_an_input(argument: str, path: str) -> ev.SpackEnvironmentError:
    """Error for a path that is neither an environment directory, a lockfile, nor a spec file."""
    if os.path.isdir(path):
        if os.path.isfile(os.path.join(path, ev.lockfile_name)):
            lockfile = os.path.join(argument, ev.lockfile_name)
            hint = f"to compare the lockfile it contains, pass '{lockfile}'"
        else:
            hint = f"an environment directory contains a '{ev.manifest_name}' file"
        return ev.SpackEnvironmentError(f"'{argument}' is not an environment directory", hint)

    if os.path.isfile(path):
        hint = (
            f"pass an environment name or directory, a '{ev.lockfile_name}' file, or a spec file"
        )
        if os.path.basename(path) == ev.manifest_name:
            directory = os.path.dirname(argument) or "."
            hint = f"to compare the environment it describes, pass '{directory}'"
        return ev.SpackEnvironmentError(f"'{argument}' is not a Spack lockfile or spec file", hint)

    if argument.endswith(_FILE_EXTENSIONS):
        return ev.SpackEnvironmentError(f"no such file: '{argument}'")

    return ev.SpackEnvironmentError(f"no such environment directory or file: '{argument}'")


def _replace_paths(text: str, paths: Tuple[str, ...], argument: str) -> str:
    for path in paths:
        text = text.replace(path, argument)
    return text


def _resolve_input(stack: contextlib.ExitStack, argument: str) -> _Input:
    """Resolve one argument to an environment or a spec, and raise if it is a path to neither an
    environment nor a spec file."""
    path = spack.config.substitute_path_variables(argument)
    # Same precedence as `spack -e`, so a file in the working directory does not shadow a name
    if ev.is_env_dir(path) or ev.exists(argument):
        env = ev.environment_from_name_or_dir(argument)
        return _Input(environment=(env, {"name": env.name, "path": env.path}))

    if os.path.isfile(path):
        # A lockfile becomes a throwaway environment, deleted when the stack is closed
        root = stack.enter_context(tempfile.TemporaryDirectory(prefix="spack-env-diff-"))
        # create_in_dir tells a lockfile from a manifest by its file name
        init_file = os.path.join(root, ev.lockfile_name)
        shutil.copy(path, init_file)
        try:
            env = ev.create_in_dir(os.path.join(root, "env"), init_file=init_file)
            # Report the lockfile, not the temporary directory, as this side's identity
            return _Input(environment=(env, {"name": None, "path": os.path.abspath(path)}))
        except ev.SpackEnvironmentError as e:
            # Parse the file only on failure, to tell what it holds
            data = _load_input_file(path)
            if _is_lockfile(data):
                # The error names the temporary copy, which is deleted before it is printed
                copies = (os.path.join(root, "env", ev.lockfile_name), init_file)
                long_message = e.long_message
                raise ev.SpackEnvironmentError(
                    _replace_paths(e.message, copies, argument),
                    _replace_paths(long_message, copies, argument) if long_message else None,
                ) from e
            if _is_specfile(data):
                return _Input(spec=spack.spec.Spec.from_dict(data))

    # A word never looks like a path, so a file or directory in the way does not hide a package
    if (os.path.exists(path) and not _is_word(argument)) or argument.endswith(_FILE_EXTENSIONS):
        raise _not_an_input(argument, path)
    spec = _standalone_spec(argument)
    # A missing path can still be spec syntax, like /hash or name/hash
    if spec is None and _looks_like_path(argument, path):
        raise _not_an_input(argument, path)
    # Only a word reaches here if the path exists
    path_error = _not_an_input(argument, path) if os.path.exists(path) else None
    return _Input(spec=spec, path_error=path_error)


def _names_a_package(name: str) -> bool:
    return spack.repo.PATH.exists(name) or spack.repo.PATH.is_virtual(name)


def _mixed_inputs(environment: str, other: str, resolved_other: _Input) -> spack.error.SpackError:
    """Error for an environment given together with an argument that is not one."""
    if resolved_other.path_error is not None:
        return resolved_other.path_error
    # A bare word next to an environment can be a spec of the same package only if it is the
    # same word, which would be an environment too
    if _is_word(other):
        return ev.SpackEnvironmentError(
            f"no environment, environment directory, or lockfile named '{other}'"
        )
    hint = None
    if _is_word(environment) and _names_a_package(environment):
        hint = (
            f"'{environment}' is an environment: to compare two specs, write it so that it does "
            "not name an environment, for instance by hash"
        )
    return spack.error.SpackError(
        f"cannot compare environment '{environment}' with spec '{other}'", hint
    )


def _resolve_inputs(stack: contextlib.ExitStack, inputs: List[str]) -> List[_Input]:
    """Resolve two arguments, or return an empty list for any other number of them, which can
    still be two specs spanning several words."""
    if len(inputs) != 2:
        return []
    resolved = [_resolve_input(stack, x) for x in inputs]
    first, second = (x.environment is not None for x in resolved)
    if first != second:
        env_index, other_index = (0, 1) if first else (1, 0)
        raise _mixed_inputs(inputs[env_index], inputs[other_index], resolved[other_index])
    return resolved


def _diff_environments(args, before: _EnvironmentInput, after: _EnvironmentInput) -> bool:
    """Compare two environments, and return whether they are equivalent."""
    env_before, identity_before = before
    env_after, identity_after = after
    label_before, label_after = args.inputs

    result = env_diff_core.diff_environments(
        env_before, env_after, prune=args.prune, label_a=label_before, label_b=label_after
    )

    if args.dump_json:
        # Keys stay positional: only the pretty output assumes a direction
        identities = {"a": identity_before, "b": identity_after}
        print(sjson.dumps({**result.as_dict(), "environments": identities}))
    else:
        EnvironmentDiffRenderer(result, label_before, label_after).render()

    return result.equivalent


def _no_match_hint(argument: str, resolved: _Input) -> Optional[str]:
    """Hint for an argument that was not an environment, and as a spec matches nothing."""
    error = resolved.path_error
    if error is not None:
        return f"{error.message}: {error.long_message}" if error.long_message else error.message
    if _is_word(argument):
        return (
            f"'{argument}' is not an environment, an environment directory, or a lockfile either"
        )
    return None


def _concrete_spec(
    spec: spack.spec.Spec, env: Optional[ev.Environment], *, no_match_hint: Optional[str]
) -> spack.spec.Spec:
    """Resolve a spec argument to the single concrete spec it matches."""
    # If the spec has a hash, check it before disambiguating
    spack.hash_lookup.replace_hash(spec)
    if spec.concrete:
        return spec
    # In an environment, its concrete specs whether installed or not
    matches = env.all_matching_specs(spec) if env else spack.store.STORE.db.query(spec)
    if not matches:
        where = f"concrete specs of environment '{env.name}'" if env else "installed packages"
        raise spack.error.SpackError(f"Spec '{spec}' matches no {where}.", no_match_hint)
    spack.cmd.ensure_single_spec_or_die(spec, matches)
    return matches[0]


def _diff_specs(args, resolved: List[_Input]) -> bool:
    """Compare two concrete specs, and return whether they are equivalent."""
    # Two arguments that are specs on their own are two specs, even if the second is a /hash
    specs = [x.spec for x in resolved if x.spec is not None]
    hints = [_no_match_hint(*x) for x in zip(args.inputs, resolved)]
    if len(specs) != 2:
        specs = spack.cmd.parse_specs(args.inputs)
        hints = [None] * len(specs)
    if len(specs) != 2:
        message = "you must provide two environments or two specs to compare"
        if len(specs) == 1 and len(args.inputs) > 1:
            # As in other commands, `hdf5 +mpi` is one spec
            message = f"'{' '.join(args.inputs)}' is a single spec: {message}"
        args.subparser.error(message)

    env = active_environment()
    before, after = (_concrete_spec(x, env, no_match_hint=h) for x, h in zip(specs, hints))
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

    return result.equivalent


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


#: A divergence and the input specs that reach it
_Entry = Tuple[spack.spec_diff.NodeDivergence, List[ev.UserSpecId]]


def _with_group(text: str, group: str) -> str:
    if group == spack.environment.environment.DEFAULT_USER_SPEC_GROUP:
        return text
    return f"{text} (group: {group})"


def _format_root(root: ev.UserSpecId, *, with_group: bool = True) -> str:
    return _with_group(str(root.spec), root.group) if with_group else str(root.spec)


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


def _group_divergences(
    divergences: List[env_diff_core.UserSpecDivergence],
) -> Tuple[Dict[str, List[_Entry]], List[_Entry]]:
    """Key divergences by group and node, and recipe changes by package, with their input specs."""
    config: Dict[str, Dict[Tuple[str, str], _Entry]] = {}  # group -> (hash of a, hash of b)
    recipes: Dict[Tuple[str, str], _Entry] = {}  # (namespace, name)

    for input_divergence in divergences:
        root = input_divergence.root
        for node in input_divergence.nodes:
            if _is_recipe_change(node):
                recipes.setdefault(_recipe_key(node), (node, []))[1].append(root)
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
    if len(roots) > _MAX_LISTED_INPUTS:
        return f"from {len(roots)} input specs"
    return "from " + ", ".join(_format_root(root, with_group=with_group) for root in roots)


class _DiffRenderer:
    """Layout shared by the environment and the spec renderers."""

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


class EnvironmentDiffRenderer(_DiffRenderer):
    """Renders an ``EnvironmentDiff`` to the terminal, for the two named environments."""

    def __init__(
        self, result: env_diff_core.EnvironmentDiff, name_before: str, name_after: str
    ) -> None:
        super().__init__(name_before, name_after)
        self.result = result

    def render(self) -> None:
        self._names()

        result = self.result
        if result.equivalent:
            self._line("the two environments are equivalent")
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

        if result.inputs.changed:
            self._section(
                "@*{Input specs changed}",
                [
                    [
                        _with_group(change.after.spec.name, change.after.group),
                        f"    {self.tag_before}{change.before.spec}",
                        f"    {self.tag_after}{change.after.spec}",
                    ]
                    for change in sorted(
                        result.inputs.changed, key=lambda x: env_diff_core.root_sort_key(x.after)
                    )
                ],
            )

        if result.providers:
            self._section(
                "@*{Input specs provided by another package}",
                [
                    [
                        _format_root(change.root),
                        f"    {self.tag_before}{change.spec_a.cformat(_PROVIDER_FORMAT)}",
                        f"    {self.tag_after}{change.spec_b.cformat(_PROVIDER_FORMAT)}",
                    ]
                    for change in sorted(
                        result.providers, key=lambda x: env_diff_core.root_sort_key(x.root)
                    )
                ],
            )

        config_by_group, recipes = _group_divergences(result.divergences)

        # Only name groups when there is more than the default one
        default = spack.environment.environment.DEFAULT_USER_SPEC_GROUP
        show_groups = list(config_by_group) != [default]

        for group, entries in config_by_group.items():
            self._section(
                f"@*{{Group: {cescape(group)}}}" if show_groups else "@*{Node differences}",
                [
                    self._node_block(
                        node, f"{node.node_a.name}  ({_reached_from(roots, with_group=False)})"
                    )
                    for node, roots in entries
                ],
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
