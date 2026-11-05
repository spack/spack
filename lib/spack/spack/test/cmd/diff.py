# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import gzip
import os
import pathlib
import shutil

import pytest

import spack.cmd.diff
import spack.concretize
import spack.environment as ev
import spack.main
import spack.paths
import spack.repo
import spack.spec
import spack.util.spack_json as sjson
import spack.util.tty.color as clr
import spack.variant
from spack import spec_diff
from spack.cmd.env import _env_create
from spack.environment import diff as env_diff_core

pytestmark = pytest.mark.usefixtures(
    "mutable_config", "mutable_mock_env_path", "mutable_mock_repo"
)

#: Marks a test that creates environments
_needs_environments = pytest.mark.not_on_windows("Envs unsupported on Windows")

install_cmd = spack.main.SpackCommand("install")
diff_cmd = spack.main.SpackCommand("diff")
find_cmd = spack.main.SpackCommand("find")
env_cmd = spack.main.SpackCommand("env")
add_cmd = spack.main.SpackCommand("add")


@pytest.fixture()
def concretized_env(tmp_path):
    """Returns a function creating a named, concretized environment from a manifest."""

    def _concretized_env(name: str, content: str) -> ev.Environment:
        manifest = tmp_path / f"{name}.yaml"
        manifest.write_text(content)
        environment = _env_create(name, init_file=str(manifest))
        with environment:
            environment.concretize()
            environment.write()
        return environment

    return _concretized_env


#: An input spec pinned to a version, so that two environments differ at its root
PINNED = "spack:\n  specs:\n  - mpileaks\n  packages:\n    mpileaks:\n      require: ['@{0}']\n"

#: `mpileaks` as a root of two groups, each pinning it to its own version
GROUPED = (
    "spack:\n"
    "  specs:\n"
    "  - group: g1\n"
    "    specs: [mpileaks]\n"
    "    override:\n"
    "      packages:\n"
    "        mpileaks:\n"
    "          require: ['@{0}']\n"
    "  - group: g2\n"
    "    specs: [mpileaks]\n"
    "    override:\n"
    "      packages:\n"
    "        mpileaks:\n"
    "          require: ['@{1}']\n"
)

#: Two input specs that both reach `mpich`, pinned to a version
SHARED_DEP = (
    "spack:\n"
    "  specs:\n"
    "  - mpileaks\n"
    "  - callpath\n"
    "  packages:\n"
    "    mpich:\n"
    "      require: ['@{0}']\n"
)


@_needs_environments
def test_diff_reports_inputs_and_divergence(concretized_env):
    """`spack diff` reports unique inputs and localizes a divergence for common inputs."""
    concretized_env("test1", "spack:\n  specs:\n  - mpileaks\n")
    concretized_env(
        "test2",
        "spack:\n"
        "  specs:\n"
        "  - mpileaks\n"
        "  - libelf\n"
        "  packages:\n"
        "    mpileaks:\n"
        "      require: ['@2.2']\n",
    )

    output = diff_cmd("test1", "test2")

    assert "libelf" in output  # an input of the second environment alone
    # The common input diverges at its root, rendered as an abstract spec holding only what differs
    assert "mpileaks@2.3" in output
    assert "mpileaks@2.2" in output


@_needs_environments
def test_diff_json(concretized_env):
    """`spack diff --json` emits a machine-readable structure."""
    concretized_env("test1", PINNED.format("2.3"))
    concretized_env("test2", PINNED.format("2.2"))

    result = sjson.load(diff_cmd("--json", "test1", "test2"))

    assert result["environments"]["a"]["name"] == "test1"
    assert result["environments"]["b"]["name"] == "test2"
    assert result["common"] == [{"spec": "mpileaks", "group": "default"}]
    names = [node["name"] for div in result["divergences"] for node in div["nodes"]]
    assert "mpileaks" in names


@_needs_environments
def test_diff_requires_concretized_environment(concretized_env):
    """`spack diff` errors clearly when an environment is not concretized."""
    env_cmd("create", "test1")
    with ev.read("test1"):
        add_cmd("libelf")  # added but never concretized
    concretized_env("test2", "spack:\n  specs:\n  - libelf\n")

    with pytest.raises(ev.SpackEnvironmentError, match="is not concretized"):
        diff_cmd("test1", "test2")


@_needs_environments
def test_diff_renders_unique_dependency(concretized_env):
    """A dependency present on one side only is rendered with the direct dependency sigil."""
    # `+openblas` adds a dependency on `openblas`, so the two roots differ both on the variant
    # and on the edge. Requiring the variant keeps `simple-inheritance` a common input spec.
    manifest = (
        "spack:\n"
        "  specs:\n"
        "  - simple-inheritance\n"
        "  packages:\n"
        "    simple-inheritance:\n"
        "      require: ['{0}']\n"
    )
    concretized_env("test1", manifest.format("~openblas"))
    concretized_env("test2", manifest.format("+openblas"))

    output = diff_cmd("test1", "test2")

    # The rendered specs are the indented lines below the header of the divergent node.
    rendered = [line.strip() for line in output.splitlines() if line.startswith("      ")]

    # The variant differs on both sides, but only the second environment has the edge.
    assert rendered[0].startswith("before: simple-inheritance~openblas/")
    assert "%openblas" not in rendered[0]
    assert rendered[1].startswith("after:  simple-inheritance+openblas/")
    assert rendered[1].endswith("%openblas")


@_needs_environments
def test_diff_groups_shared_divergent_node(concretized_env):
    """A node reached from several input specs is reported once, listing the input specs."""
    concretized_env("test1", SHARED_DEP.format("3.0.4"))
    concretized_env("test2", SHARED_DEP.format("1.0"))

    output = diff_cmd("test1", "test2")

    # Reported once, not once per input spec, and the input specs in a canonical order
    assert output.count("before: mpich@3.0.4/") == 1
    assert output.count("after:  mpich@1.0/") == 1
    assert "mpich  (from callpath, mpileaks)" in output


@_needs_environments
def test_diff_reports_count_for_many_shared_inputs(concretized_env, monkeypatch):
    """Past a threshold, the input specs reaching a divergent node are counted, not listed."""
    monkeypatch.setattr(spack.cmd.diff, "_MAX_LISTED_INPUTS", 1)
    concretized_env("test1", SHARED_DEP.format("3.0.4"))
    concretized_env("test2", SHARED_DEP.format("1.0"))

    assert "mpich  (from 2 input specs)" in diff_cmd("test1", "test2")


@_needs_environments
def test_diff_distinguishes_groups(concretized_env):
    """Roots of different groups are compared separately, not collapsed by abstract spec."""
    # The abstract spec is `mpileaks` in all four roots, so only the group tells them apart
    concretized_env("test1", GROUPED.format("2.3", "2.2"))
    concretized_env("test2", GROUPED.format("2.3", "2.1"))

    output = diff_cmd("test1", "test2")

    # `g1` pins the same version in both environments, so neither it nor its section shows up.
    # Only `g2` diverges, and its section header is what tells its root from the `g1` one.
    assert "Group: g2" in output
    assert "mpileaks  (from mpileaks)" in output
    assert "before: mpileaks@2.2/" in output
    assert "after:  mpileaks@2.1/" in output
    assert "Group: g1" not in output
    assert "2.3" not in output


def test_diff_merges_recipe_changes_per_package(capsys):
    """Recipe changes are merged per package, since a package hash is per instance.

    Two differently configured instances of the same package yield different package hashes for
    a single edit to its recipe, so keying them by hash would report that one edit twice.
    """
    first = spack.concretize.concretize_one("mpich@3.0.4")
    second = spack.concretize.concretize_one("mpich@1.0")
    recipe = spec_diff.DiffCategory.RECIPE

    output = _render(
        capsys,
        _user_spec_divergence(
            "mpileaks", _divergence(first, first, recipe, value_a="aaa", value_b="bbb")
        ),
        _user_spec_divergence(
            "callpath", _divergence(second, second, recipe, value_a="ccc", value_b="ddd")
        ),
    )

    # Both instances are merged into one entry, and their input specs ordered canonically
    assert output.count("mpich  (") == 1
    assert "mpich  (from callpath, mpileaks)" in output
    # Recipe changes span groups, so they are kept apart from the per-group configuration ones
    assert "Node differences" not in output


@_needs_environments
def test_diff_sections_differences_by_group(concretized_env):
    """Configuration differences are reported under the group of the input spec reaching them."""
    # Both groups diverge, so each section has to show its own difference
    concretized_env("test1", GROUPED.format("2.3", "2.2"))
    concretized_env("test2", GROUPED.format("2.2", "2.1"))

    sections = diff_cmd("test1", "test2").split("-- Group: ")

    # Sections are sorted by group name, the order groups concretize in not being stable
    assert len(sections) == 3  # the header, then one section per group
    assert sections[1].startswith("g1")
    assert "before: mpileaks@2.3/" in sections[1] and "after:  mpileaks@2.2/" in sections[1]
    assert sections[2].startswith("g2")
    assert "before: mpileaks@2.2/" in sections[2] and "after:  mpileaks@2.1/" in sections[2]


@_needs_environments
def test_diff_no_prune_reports_downstream_differences(concretized_env):
    """`--no-prune` reports the consequences of a difference, not just the first one found."""
    # `dyninst` is reached only through `callpath`, which itself differs between the two
    manifest = (
        "spack:\n"
        "  specs:\n"
        "  - mpileaks\n"
        "  packages:\n"
        "    callpath:\n"
        "      require: ['@{0}']\n"
        "    dyninst:\n"
        "      require: ['@{1}']\n"
    )
    concretized_env("test1", manifest.format("1.0", "8.2"))
    concretized_env("test2", manifest.format("0.9", "8.1.2"))

    pruned = diff_cmd("test1", "test2")
    assert "callpath" in pruned
    assert "dyninst" not in pruned

    full = diff_cmd("--no-prune", "test1", "test2")
    assert "callpath" in full
    assert "before: dyninst@8.2/" in full
    assert "after:  dyninst@8.1.2/" in full


@_needs_environments
@pytest.mark.parametrize("lockfile", ["v1", "v2", "v3"])
def test_diff_refuses_environments_without_package_hashes(concretized_env, lockfile):
    """Environments from lockfiles older than package hashes are refused, not crashed on."""
    env_cmd(
        "create",
        "old",
        os.path.join(spack.paths.test_path, "data", "legacy_env", f"{lockfile}.lock"),
    )
    concretized_env("new", "spack:\n  specs:\n  - mpileaks\n")

    with pytest.raises(ev.SpackEnvironmentError, match="did not record package hashes"):
        diff_cmd("old", "new")


@_needs_environments
def test_diff_accepts_a_concretized_empty_environment(concretized_env):
    """An environment with nothing to concretize is comparable, not "not concretized"."""
    concretized_env("test1", "spack:\n  specs: []\n")
    concretized_env("test2", "spack:\n  specs: []\n")

    assert "equivalent" in diff_cmd("test1", "test2")


@_needs_environments
def test_diff_refuses_a_partially_concretized_environment(concretized_env):
    """A spec added after the last concretization is refused, not dropped from the comparison."""
    concretized_env("test1", "spack:\n  specs:\n  - mpileaks\n")
    concretized_env("test2", "spack:\n  specs:\n  - mpileaks\n")

    # `test1` has a concretized root, so the environment looks concretized at a glance
    with ev.read("test1"):
        add_cmd("libelf")

    with pytest.raises(ev.SpackEnvironmentError, match="is not concretized") as exc_info:
        diff_cmd("test1", "test2")

    assert "libelf" in str(exc_info.value)


@_needs_environments
def test_diff_json_is_ordered_canonically(concretized_env):
    """`--json` does not inherit the order the environment happened to concretize its roots in."""
    # Three groups with no dependency between them are concretized in an unspecified order, so
    # the roots reach the diff in an order that varies between runs.
    concretized_env(
        "test1",
        "spack:\n"
        "  specs:\n"
        "  - group: g1\n"
        "    specs: [libelf]\n"
        "  - group: g2\n"
        "    specs: [libdwarf]\n"
        "  - group: g3\n"
        "    specs: [mpich]\n",
    )
    concretized_env("test2", "spack:\n  specs: []\n")

    result = sjson.load(diff_cmd("--json", "test1", "test2"))

    assert [(x["group"], x["spec"]) for x in result["only_in_a"]] == [
        ("g1", "libelf"),
        ("g2", "libdwarf"),
        ("g3", "mpich"),
    ]


@_needs_environments
def test_diff_reports_a_differing_external(concretized_env):
    """An external found at a different prefix is named, not left unexplained."""
    # `libelf` is used rather than one of the `external*` mock packages because those are already
    # declared external by the mock configuration. Externals merge across scopes, so a manifest
    # naming the same spec adds a second, equally good candidate instead of replacing the first,
    # and which of the two the solver picks is not pinned by anything: the two environments can
    # then land on the same prefix and have nothing to differ about.
    manifest = (
        "spack:\n"
        "  specs:\n"
        "  - libelf\n"
        "  packages:\n"
        "    libelf:\n"
        "      buildable: false\n"
        "      externals:\n"
        "      - spec: libelf@0.8.13\n"
        "        prefix: {0}\n"
    )
    concretized_env("test1", manifest.format("/usr/local"))
    concretized_env("test2", manifest.format("/opt/local"))

    output = diff_cmd("test1", "test2")

    # Nothing about the configuration differs, so this used to land in the unresolved bucket
    assert "no difference to point at" not in output
    assert "external path" in output
    assert "/opt/local" in output


def _divergence(node_a, node_b, category, key="", value_a="", value_b=""):
    """A divergence whose only reported difference is one attribute of the two nodes."""
    attribute = spec_diff.AttributeDiff(category, key, value_a, value_b)
    return spec_diff.NodeDivergence(node_a, node_b, [attribute])


def _user_spec_divergence(
    root: str, *nodes: spec_diff.NodeDivergence
) -> env_diff_core.UserSpecDivergence:
    """Divergent nodes reached from one input spec of the default group."""
    return env_diff_core.UserSpecDivergence(
        ev.UserSpecId("default", spack.spec.Spec(root)), list(nodes)
    )


def _render(capsys, *divergences: env_diff_core.UserSpecDivergence, color: bool = False) -> str:
    """Render divergences of common input specs the way `spack diff` does."""
    result = env_diff_core.EnvironmentDiff(
        inputs=env_diff_core.InputDiff(
            only_in_a=[], only_in_b=[], common=[x.root for x in divergences]
        ),
        divergences=list(divergences),
        unresolved=[],
    )
    with clr.color_when(color):
        spack.cmd.diff.EnvironmentDiffRenderer(result, "e1", "e2").render()
    return capsys.readouterr().out


def test_diff_renders_recipe_changes(capsys):
    """The recipe section cannot be reached end to end, since a recipe cannot be changed midway.

    Two environments concretized in one process share their package files, so the only way to a
    differing package hash is a lockfile written by another Spack, which the command refuses.
    """
    mpich = spack.concretize.concretize_one("mpich@3.0.4")
    divergence = _divergence(
        mpich, mpich, spec_diff.DiffCategory.RECIPE, value_a="aaa", value_b="bbb"
    )

    output = _render(capsys, _user_spec_divergence("mpileaks", divergence))

    assert "Packages whose recipe differs" in output
    assert "mpich  (from mpileaks)" in output
    # the two configurations are identical, so there is no pair of specs worth showing
    assert "before: mpich" not in output


def test_diff_renders_an_unresolved_input(capsys):
    """The bucket for a difference nothing accounts for is reported rather than swallowed."""
    root = ev.UserSpecId("default", spack.spec.Spec("mpileaks"))
    result = env_diff_core.EnvironmentDiff(
        inputs=env_diff_core.InputDiff(only_in_a=[], only_in_b=[], common=[root]),
        divergences=[],
        unresolved=[root],
    )

    spack.cmd.diff.EnvironmentDiffRenderer(result, "e1", "e2").render()

    output = capsys.readouterr().out
    assert "no difference to point at" in output
    assert "mpileaks" in output
    assert "equivalent" not in output


def test_diff_renders_only_the_differing_architecture_part(capsys, mutable_mock_repo):
    """Architecture parts are rendered one part at a time."""
    node = spack.concretize.concretize_one("mpich@3.0.4")
    divergence = _divergence(
        node, node, spec_diff.DiffCategory.ARCHITECTURE, "os", "debian6", "ubuntu99"
    )

    output = _render(capsys, _user_spec_divergence("mpileaks", divergence))

    # only the differing part is shown, and the version, which does not differ, is hidden
    assert f"os={node.architecture.os}" in output
    assert f"target={node.architecture.target}" not in output
    assert "@3.0.4" not in output


def _concretized_directory_env(directory: pathlib.Path, content: str) -> ev.Environment:
    """Create an independent environment in a directory from a manifest, and concretize it."""
    directory.mkdir()
    (directory / ev.manifest_name).write_text(content)
    environment = ev.Environment(str(directory))
    with environment:
        environment.concretize()
        environment.write()
    return environment


@_needs_environments
def test_diff_accepts_environment_directories(tmp_path):
    """Both arguments are a name or a directory, and directories were only ever the former."""
    _concretized_directory_env(tmp_path / "d1", PINNED.format("2.3"))
    _concretized_directory_env(tmp_path / "d2", PINNED.format("2.2"))

    output = diff_cmd(str(tmp_path / "d1"), str(tmp_path / "d2"))

    assert "before: mpileaks@2.3/" in output
    assert "after:  mpileaks@2.2/" in output


@_needs_environments
def test_diff_orders_input_specs_the_same_way_everywhere(concretized_env):
    """The text and the json output must not disagree on the order of the same list."""
    # Sorting the rendered strings and sorting by (group, spec) part ways as soon as groups are
    # involved, since the group is rendered as a suffix.
    concretized_env(
        "test1",
        "spack:\n"
        "  specs:\n"
        "  - group: g2\n"
        "    specs: [libelf]\n"
        "  - group: g1\n"
        "    specs: [mpich]\n",
    )
    concretized_env("test2", "spack:\n  specs: []\n")

    from_json = [x["spec"] for x in sjson.load(diff_cmd("--json", "test1", "test2"))["only_in_a"]]

    output = diff_cmd("test1", "test2")
    lines = [
        line.strip() for line in output.splitlines() if line.startswith("  ") and line.strip()
    ]
    from_text = [line.split(" ")[0] for line in lines if line.split(" ")[0] in from_json]

    assert from_json == ["mpich", "libelf"]  # g1 before g2
    assert from_text == from_json


@pytest.mark.parametrize(
    "version_a,version_b,color",
    [
        # A newer version is what one expects of a re-concretization, so it is not highlighted
        ("3.0.3", "3.0.4", spack.spec.VERSION_COLOR),
        # Going back to an older version is what the output exists to point at
        ("3.0.4", "3.0.3", spack.spec.HIGHLIGHT_COLOR),
    ],
)
def test_diff_highlights_only_a_version_regression(
    version_a, version_b, color, capsys, mutable_mock_repo
):
    """Tests that the style of a version change depends on its direction, on both sides."""
    node_a = spack.concretize.concretize_one(f"mpich@{version_a}")
    node_b = spack.concretize.concretize_one(f"mpich@{version_b}")
    divergence = _divergence(node_a, node_b, spec_diff.DiffCategory.VERSION)

    output = _render(capsys, _user_spec_divergence("mpileaks", divergence), color=True)

    assert clr.colorize(f"{color}@@{version_a}@.", color=True) in output
    assert clr.colorize(f"{color}@@{version_b}@.", color=True) in output


@pytest.mark.parametrize(
    "starts_from,lands_on,color",
    [
        # A variant that ends up at the value the package declares is an expected change
        ("+debug", "~debug", spack.spec.VARIANT_COLOR),
        # A variant that ends up on a non-default value is worth pointing at
        ("~debug", "+debug", spack.spec.HIGHLIGHT_COLOR),
    ],
)
def test_diff_styles_a_variant_by_the_value_it_lands_on(
    starts_from, lands_on, color, capsys, mutable_mock_repo
):
    """The style of a variant change is judged on the value the second side lands on."""
    node_a = spack.concretize.concretize_one(f"mpich@3.0.4{starts_from}")
    node_b = spack.concretize.concretize_one(f"mpich@3.0.4{lands_on}")
    divergence = _divergence(node_a, node_b, spec_diff.DiffCategory.VARIANT, "debug")

    output = _render(capsys, _user_spec_divergence("mpileaks", divergence), color=True)

    assert clr.colorize(f"{color}{starts_from}@.", color=True) in output
    assert clr.colorize(f"{color}{lands_on}@.", color=True) in output


@pytest.mark.parametrize(
    "variant,color", [("~debug", spack.spec.VARIANT_COLOR), ("+debug", spack.spec.HIGHLIGHT_COLOR)]
)
def test_diff_styles_a_variant_absent_on_the_second_side(
    variant, color, capsys, mutable_mock_repo
):
    """A variant only the first side has is judged on the only value the diff has to show."""
    node_a = spack.concretize.concretize_one(f"mpich@3.0.4{variant}")
    node_b = spack.concretize.concretize_one("libelf")
    assert "debug" not in node_b.variants
    divergence = _divergence(node_a, node_b, spec_diff.DiffCategory.VARIANT, "debug")

    output = _render(capsys, _user_spec_divergence("mpileaks", divergence), color=True)

    assert clr.colorize(f"{color}{variant}@.", color=True) in output


def test_diff_highlights_a_variant_the_package_no_longer_declares(capsys, mutable_mock_repo):
    """A node recorded with a variant its package does not declare has no default to judge by."""
    node_a = spack.concretize.concretize_one("mpich@3.0.4")
    node_b = spack.concretize.concretize_one("mpich@3.0.4")
    node_b.variants.set(spack.variant.BoolValuedVariant("gone", True))
    divergence = _divergence(node_a, node_b, spec_diff.DiffCategory.VARIANT, "gone")

    output = _render(capsys, _user_spec_divergence("mpileaks", divergence), color=True)

    assert clr.colorize(f"{spack.spec.HIGHLIGHT_COLOR}+gone@.", color=True) in output


def test_diff_highlights_a_variant_of_a_package_no_longer_in_the_repository(
    capsys, mutable_mock_repo, monkeypatch
):
    """An environment can have been concretized against a repository we no longer have."""
    node_a = spack.concretize.concretize_one("mpich@3.0.4+debug")
    node_b = spack.concretize.concretize_one("mpich@3.0.4~debug")
    divergence = _divergence(node_a, node_b, spec_diff.DiffCategory.VARIANT, "debug")

    def unknown(spec):
        raise spack.repo.UnknownPackageError(spec.name)

    monkeypatch.setattr(spack.repo.PATH, "get", unknown)

    output = _render(capsys, _user_spec_divergence("mpileaks", divergence), color=True)

    # ~debug is the default, but with no package to read it from the change stays highlighted
    assert clr.colorize(f"{spack.spec.HIGHLIGHT_COLOR}~debug@.", color=True) in output


@_needs_environments
def test_diff_json_is_versioned_and_names_the_environments(concretized_env, tmp_path):
    """`spack diff --json` includes a format version, and the identity of what it compared."""
    concretized_env("test1", PINNED.format("2.3"))

    # The second environment is independent, so the two identities are of different kinds
    directory = tmp_path / "independent"
    independent = _concretized_directory_env(directory, PINNED.format("2.2"))

    result = sjson.load(diff_cmd("--json", "test1", str(directory)))

    assert result["_meta"] == {
        "file-type": "spack-environment-diff",
        "diff-version": spec_diff.DIFF_FORMAT_VERSION,
    }

    # A managed environment is named, an independent one is identified by its directory. Either
    # way the identities are stored in their own block, so they cannot collide with the comparison.
    assert result["environments"]["a"] == {"name": "test1", "path": ev.read("test1").path}
    assert result["environments"]["b"] == {"name": independent.name, "path": independent.path}
    assert "environments" not in result["_meta"]


@_needs_environments
def test_diff_accepts_lockfile_paths(concretized_env, tmp_path):
    """Two lockfiles can be compared directly, without creating an environment for each first."""
    before = concretized_env("test1", PINNED.format("2.3"))
    after = concretized_env("test2", PINNED.format("2.2"))

    # As a user who downloaded two lockfiles would have them: files, outside any environment
    first = tmp_path / "first.lock"
    second = tmp_path / "second.lock"
    shutil.copy(before.lock_path, first)
    shutil.copy(after.lock_path, second)

    output = diff_cmd(str(first), str(second))

    # The same divergence the two environments themselves report
    assert "mpileaks@2.3" in output
    assert "mpileaks@2.2" in output


@_needs_environments
def test_diff_reports_a_lockfile_by_the_path_it_was_given(concretized_env, tmp_path):
    """The throwaway environment a lockfile is read through never surfaces in the output."""
    before = concretized_env("test1", PINNED.format("2.3"))
    after = concretized_env("test2", PINNED.format("2.2"))
    lockfile = tmp_path / "downloaded.lock"
    shutil.copy(after.lock_path, lockfile)

    result = sjson.load(diff_cmd("--json", "test1", str(lockfile)))

    # A managed environment keeps its name; a lockfile is identified by the file itself, since
    # the directory it is materialized in is temporary and gone by the time this is read.
    assert result["environments"]["a"] == {"name": "test1", "path": before.path}
    assert result["environments"]["b"] == {"name": None, "path": str(lockfile)}


@_needs_environments
def test_diff_mixes_an_environment_and_a_lockfile(concretized_env, tmp_path):
    """The two sides are resolved independently, so they need not be of the same kind."""
    concretized_env("test1", PINNED.format("2.3"))
    after = concretized_env("test2", PINNED.format("2.2"))
    lockfile = tmp_path / "downloaded.lock"
    shutil.copy(after.lock_path, lockfile)

    from_lockfile = diff_cmd("test1", str(lockfile))
    from_environment = diff_cmd("test1", "test2")

    # Reading the second side from its lockfile finds what reading it as an environment finds
    assert "mpileaks@2.2" in from_lockfile
    assert from_lockfile.split("\n")[3:] == from_environment.split("\n")[3:]


@_needs_environments
def test_diff_names_the_lockfile_it_refuses(concretized_env, tmp_path):
    """A lockfile that cannot be compared is named by its path, not by a temporary directory."""
    concretized_env("test1", "spack:\n  specs:\n  - mpileaks\n")
    legacy = tmp_path / "old.lock"
    shutil.copy(os.path.join(spack.paths.test_path, "data", "legacy_env", "v1.lock"), legacy)

    with pytest.raises(ev.SpackEnvironmentError, match="did not record package hashes") as exc:
        diff_cmd(str(legacy), "test1")

    assert str(legacy) in str(exc.value)


@_needs_environments
def test_diff_refuses_a_manifest_path(concretized_env, tmp_path):
    """A manifest is not a lockfile, and the error points at the directory to pass instead."""
    concretized_env("test1", PINNED.format("2.3"))
    directory = tmp_path / "independent"
    directory.mkdir()
    manifest = directory / ev.manifest_name
    manifest.write_text(PINNED.format("2.2"))

    with pytest.raises(ev.SpackEnvironmentError, match="is not a Spack lockfile") as exc:
        diff_cmd("test1", str(manifest))

    assert str(directory) in str(exc.value)


@_needs_environments
def test_diff_refuses_a_file_that_is_not_a_lockfile(concretized_env, tmp_path):
    """A file is accepted for what it contains, not for how it is named."""
    concretized_env("test1", PINNED.format("2.3"))
    not_a_lockfile = tmp_path / "notes.txt"
    not_a_lockfile.write_text("mpileaks@2.2\n")

    with pytest.raises(ev.SpackEnvironmentError, match="is not a Spack lockfile"):
        diff_cmd("test1", str(not_a_lockfile))


@_needs_environments
def test_diff_accepts_a_lockfile_whose_name_is_not_a_lockfile_name(concretized_env, tmp_path):
    """A lockfile downloaded under any name is still compared as a lockfile."""
    concretized_env("test1", PINNED.format("2.3"))
    after = concretized_env("test2", PINNED.format("2.2"))
    renamed = tmp_path / "downloaded-lockfile.txt"
    shutil.copy(after.lock_path, renamed)

    output = diff_cmd("test1", str(renamed))

    assert "mpileaks@2.3" in output
    assert "mpileaks@2.2" in output


def test_diff_names_the_flag_to_compare_specs():
    """Arguments are environments by default, and the error for a spec names the flag to use."""
    with pytest.raises(ev.SpackEnvironmentError, match="no environment") as exc:
        diff_cmd("mpileaks", "mpileaks+debug")

    assert "spack diff --specs" in exc.value.long_message


@_needs_environments
@pytest.mark.parametrize("arguments", [["test1"], ["test1", "test1", "test1"]])
def test_diff_requires_two_environments(concretized_env, arguments):
    """Comparing anything but two environments is a usage error."""
    concretized_env("test1", PINNED.format("2.3"))

    with pytest.raises(spack.main.SpackCommandError) as exc:
        diff_cmd(*arguments)

    assert exc.value.code == 2


def _install_and_find(spec: str) -> str:
    """Install a spec and return the hash of the installation matching it."""
    install_cmd("--fake", spec)
    return find_cmd("--format", "{/hash}", spec).strip()


def test_diff_specs_reports_a_differing_dependency(install_mockery, mock_fetch, mock_archive):
    """Two installations of a package that differ below the root are compared node by node."""
    before = _install_and_find("mpileaks ^mpich@3.0.4")
    after = _install_and_find("mpileaks ^mpich@1.0")

    output = diff_cmd("--specs", before, after)

    assert "before: mpich@3.0.4/" in output
    assert "after:  mpich@1.0/" in output
    # Specs have no input specs, so nodes are not attributed to any
    assert "(from" not in output


def test_diff_specs_json(install_mockery, mock_fetch, mock_archive):
    """`spack diff --specs --json` is versioned, and names the two specs it compared."""
    before = _install_and_find("mpileaks ^mpich@3.0.4")
    after = _install_and_find("mpileaks ^mpich@1.0")

    result = sjson.load(diff_cmd("--specs", "--json", before, after))

    assert result["_meta"] == {
        "file-type": "spack-spec-diff",
        "diff-version": spec_diff.DIFF_FORMAT_VERSION,
    }
    assert [node["name"] for node in result["nodes"]] == ["mpich"]
    assert result["specs"]["a"] == {"name": "mpileaks", "hash": before[1:]}
    assert result["specs"]["b"] == {"name": "mpileaks", "hash": after[1:]}


def test_diff_specs_reports_identical_specs(install_mockery, mock_fetch, mock_archive):
    """A spec compared with itself is reported as such."""
    installed = _install_and_find("mpileaks")

    assert "the two specs are identical" in diff_cmd("--specs", installed, installed)
    assert sjson.load(diff_cmd("--specs", "--json", installed, installed))["nodes"] == []


def test_diff_specs_refuses_an_ambiguous_spec(install_mockery, mock_fetch, mock_archive):
    """A spec matching several installations fails, listing the candidates."""
    first = _install_and_find("mpileaks ^mpich@3.0.4")
    second = _install_and_find("mpileaks ^mpich@1.0")

    with pytest.raises(spack.main.SpackCommandError) as exc:
        diff_cmd("--specs", "mpileaks", "mpileaks")

    assert exc.value.code == 1
    assert first[1:8] in exc.value.output and second[1:8] in exc.value.output


def test_diff_specs_refuses_specs_of_different_packages(install_mockery, mock_fetch, mock_archive):
    """Two specs of different packages have no node in common to compare."""
    mpileaks = _install_and_find("mpileaks")
    mpich = find_cmd("--format", "{/hash}", "mpich").strip()

    with pytest.raises(spec_diff.SpecDiffError, match="must be of the same package"):
        diff_cmd("--specs", mpileaks, mpich)


@pytest.mark.parametrize("arguments", [["mpileaks"], ["mpileaks", "+debug"]])
def test_diff_specs_requires_two_specs(arguments):
    """Specs are counted after parsing, so a spec spanning several words counts once."""
    with pytest.raises(spack.main.SpackCommandError) as exc:
        diff_cmd("--specs", *arguments)

    assert exc.value.code == 2


def test_diff_specs_refuses_specs_without_package_hashes(tmp_path):
    """Spec files written before package hashes existed are refused, as environments are."""
    paths = []
    for version in ("v017", "v019"):
        source = os.path.join(
            spack.paths.test_path, "data", "specfiles", f"hdf5.{version}.json.gz"
        )
        with gzip.open(source, "rt", encoding="utf-8") as stream:
            path = tmp_path / f"hdf5.{version}.json"
            path.write_text(stream.read())
        paths.append(str(path))

    with pytest.raises(spec_diff.SpecDiffError, match="did not record package hashes"):
        diff_cmd("--specs", *paths)


def test_diff_specs_lists_recipe_changes_by_package(capsys):
    """A recipe change has no configuration to show, so only the package is named."""
    before = spack.concretize.concretize_one("mpileaks")
    after = spack.concretize.concretize_one("mpileaks+debug")
    recipe = spec_diff.DiffCategory.RECIPE
    nodes = [
        _divergence(before["mpich"], before["mpich"], recipe, value_a="aaa", value_b="bbb"),
        _divergence(before["callpath"], before["callpath"], recipe, value_a="ccc", value_b="ddd"),
    ]

    spack.cmd.diff.SpecDiffRenderer(spec_diff.SpecDiff(before, after, nodes), "s1", "s2").render()

    output = capsys.readouterr().out
    assert "Packages whose recipe differs" in output
    assert "Node differences" not in output
    assert output.index("callpath") < output.index("mpich")


@_needs_environments
@pytest.mark.parametrize(
    "after,exit_code",
    [(PINNED.format("2.3"), 0), (PINNED.format("2.2"), spack.cmd.diff.EXIT_DIFFERENT)],
)
@pytest.mark.parametrize("output", [[], ["--json"]])
def test_diff_exit_code_tells_whether_environments_differ(
    concretized_env, after, exit_code, output
):
    """With `--exit-code`, a script can tell differing environments from an error."""
    concretized_env("test1", PINNED.format("2.3"))
    concretized_env("test2", after)

    diff_cmd(*output, "test1", "test2")
    assert diff_cmd.returncode == 0

    diff_cmd(*output, "--exit-code", "test1", "test2", fail_on_error=False)
    assert diff_cmd.returncode == exit_code


def test_diff_exit_code_tells_whether_specs_differ(install_mockery, mock_fetch, mock_archive):
    """With `--exit-code`, a script can tell differing specs from an error."""
    before = _install_and_find("mpileaks ^mpich@3.0.4")
    after = _install_and_find("mpileaks ^mpich@1.0")

    diff_cmd("--specs", "--exit-code", before, before)
    assert diff_cmd.returncode == 0

    diff_cmd("--specs", "--exit-code", before, after, fail_on_error=False)
    assert diff_cmd.returncode == spack.cmd.diff.EXIT_DIFFERENT
