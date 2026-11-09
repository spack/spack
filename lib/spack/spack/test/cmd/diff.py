# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import gzip
import os

import pytest

import spack.cmd.diff
import spack.concretize
import spack.environment as ev
import spack.error
import spack.main
import spack.paths
import spack.repo
import spack.spec
import spack.util.spack_json as sjson
import spack.util.tty.color as clr
import spack.variant
from spack import spec_diff
from spack.cmd.env import _env_create

pytestmark = pytest.mark.usefixtures(
    "mutable_config", "mutable_mock_env_path", "mutable_mock_repo"
)

#: Marks a test that creates environments
_needs_environments = pytest.mark.not_on_windows("Envs unsupported on Windows")

install_cmd = spack.main.SpackCommand("install")
diff_cmd = spack.main.SpackCommand("diff")
find_cmd = spack.main.SpackCommand("find")


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


def _divergence(node_a, node_b, category, key="", value_a="", value_b=""):
    """A divergence whose only reported difference is one attribute of the two nodes."""
    attribute = spec_diff.AttributeDiff(category, key, value_a, value_b)
    return spec_diff.NodeDivergence(node_a, node_b, [attribute])


def _render_node(capsys, divergence: spec_diff.NodeDivergence, color: bool = False) -> str:
    """Render one divergent node the way `spack diff` does."""
    result = spec_diff.SpecDiff(divergence.node_a, divergence.node_b, [divergence])
    with clr.color_when(color):
        spack.cmd.diff.SpecDiffRenderer(result, "s1", "s2").render()
    return capsys.readouterr().out


def _styled(color: str, text: str) -> str:
    """The text in the given color, as the renderer writes it to a terminal."""
    return clr.colorize(f"{color}{text}@.", color=True)


def test_diff_renders_only_the_differing_architecture_part(capsys, mutable_mock_repo):
    """Architecture parts are rendered one part at a time."""
    node = spack.concretize.concretize_one("mpich@3.0.4~debug")
    other = spack.concretize.concretize_one("mpich@3.0.4+debug")
    divergence = _divergence(
        node, other, spec_diff.DiffCategory.ARCHITECTURE, "os", "debian6", "ubuntu99"
    )

    output = _render_node(capsys, divergence)

    # only the differing part is shown, and the version, which does not differ, is hidden
    assert f"os={node.architecture.os}" in output
    assert f"target={node.architecture.target}" not in output
    assert "@3.0.4" not in output


@pytest.mark.parametrize(
    "version_a,version_b,color",
    [
        # A newer version is what one expects of a re-concretization, so it is not highlighted
        ("3.0.3", "3.0.4", spack.spec.VERSION_COLOR),
        # Going back to an older version is highlighted
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

    output = _render_node(capsys, divergence, color=True)

    assert _styled(color, f"@@{version_a}") in output
    assert _styled(color, f"@@{version_b}") in output


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

    output = _render_node(capsys, divergence, color=True)

    assert _styled(color, starts_from) in output
    assert _styled(color, lands_on) in output


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

    output = _render_node(capsys, divergence, color=True)

    assert _styled(color, variant) in output


def test_diff_highlights_a_variant_the_package_no_longer_declares(capsys, mutable_mock_repo):
    """A node recorded with a variant its package does not declare has no default to judge by."""
    node_a = spack.concretize.concretize_one("mpich@3.0.4~debug")
    node_b = spack.concretize.concretize_one("mpich@3.0.4+debug")
    node_b.variants.set(spack.variant.BoolValuedVariant("gone", True))
    divergence = _divergence(node_a, node_b, spec_diff.DiffCategory.VARIANT, "gone")

    output = _render_node(capsys, divergence, color=True)

    assert _styled(spack.spec.HIGHLIGHT_COLOR, "+gone") in output


def test_diff_highlights_a_variant_of_a_package_no_longer_in_the_repository(
    capsys, mutable_mock_repo, monkeypatch
):
    """A variant of a package missing from the repository is highlighted, with no default."""
    node_a = spack.concretize.concretize_one("mpich@3.0.4+debug")
    node_b = spack.concretize.concretize_one("mpich@3.0.4~debug")
    divergence = _divergence(node_a, node_b, spec_diff.DiffCategory.VARIANT, "debug")

    def unknown(spec):
        raise spack.repo.UnknownPackageError(spec.name)

    monkeypatch.setattr(spack.repo.PATH, "get", unknown)

    output = _render_node(capsys, divergence, color=True)

    # ~debug is the default, but with no package to read it from the change stays highlighted
    assert _styled(spack.spec.HIGHLIGHT_COLOR, "~debug") in output


def _install_and_find(spec: str) -> str:
    """Install a spec and return the hash of the installation matching it."""
    install_cmd("--fake", spec)
    return find_cmd("--format", "{/hash}", spec).strip()


def test_diff_specs_reports_a_differing_dependency(install_mockery, mock_fetch, mock_archive):
    """Two installations of a package that differ below the root are compared node by node."""
    before = _install_and_find("mpileaks ^mpich@3.0.4")
    after = _install_and_find("mpileaks ^mpich@1.0")

    output = diff_cmd(before, after)

    assert "before: mpich@3.0.4/" in output
    assert "after:  mpich@1.0/" in output
    # Specs have no input specs, so nodes are not attributed to any
    assert "(from" not in output


def test_diff_specs_json(install_mockery, mock_fetch, mock_archive):
    """`spack diff --json` is versioned, and names the two specs it compared."""
    before = _install_and_find("mpileaks ^mpich@3.0.4")
    after = _install_and_find("mpileaks ^mpich@1.0")

    result = sjson.load(diff_cmd("--json", before, after))

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

    assert "the two specs are identical" in diff_cmd(installed, installed)
    assert sjson.load(diff_cmd("--json", installed, installed))["nodes"] == []


def test_diff_specs_refuses_an_ambiguous_spec(install_mockery, mock_fetch, mock_archive):
    """A spec matching several installations fails, listing the candidates."""
    first = _install_and_find("mpileaks ^mpich@3.0.4")
    second = _install_and_find("mpileaks ^mpich@1.0")

    with pytest.raises(spack.main.SpackCommandError) as exc:
        diff_cmd("mpileaks", "mpileaks")

    assert exc.value.code == 1
    assert first[1:8] in exc.value.output and second[1:8] in exc.value.output


def test_diff_specs_refuses_specs_of_different_packages(install_mockery, mock_fetch, mock_archive):
    """Two specs of different packages have no node in common to compare."""
    mpileaks = _install_and_find("mpileaks")
    mpich = find_cmd("--format", "{/hash}", "mpich").strip()

    with pytest.raises(spec_diff.SpecDiffError, match="must be of the same package"):
        diff_cmd(mpileaks, mpich)


@pytest.mark.parametrize("arguments", [["mpileaks"], ["mpileaks", "+debug"]])
def test_diff_specs_requires_two_specs(arguments):
    """Specs are counted after parsing, so a spec spanning several words counts once."""
    with pytest.raises(spack.main.SpackCommandError) as exc:
        diff_cmd(*arguments)

    assert exc.value.code == 2


def test_diff_specs_refuses_specs_without_package_hashes(tmp_path):
    """Spec files written before package hashes existed are refused."""
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
        diff_cmd(*paths)


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
def test_diff_specs_compares_specs_of_an_environment_that_is_not_installed(concretized_env):
    """In an active environment, a spec is matched against its concrete specs, installed or
    not."""
    content = "spack:\n  concretizer:\n    unify: false\n  specs: [mpileaks@2.3, mpileaks@2.2]\n"
    environment = concretized_env("test1", content)

    with environment:
        output = diff_cmd("mpileaks@2.3", "mpileaks@2.2")

        with pytest.raises(spack.error.SpackError, match="no concrete specs of environment"):
            diff_cmd("mpileaks@2.3", "mpileaks@2.1")

    assert "before: mpileaks@2.3/" in output
    assert "after:  mpileaks@2.2/" in output
