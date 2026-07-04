# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import os
import shutil

import pytest

import spack.concretize
import spack.environment as ev
import spack.main
import spack.paths
import spack.repo
import spack.stage
from spack.main import SpackCommand
from spack.util.filesystem import mkdirp

# `spack path` is the canonical command; `spack location` is a deprecated alias
# that shares the same parser and directory-resolution logic. The only behavioral
# differences are the default (no-option) directory and the deprecation notice in
# `location`'s help, so the shared option tests below run through `spack path`.

# Everything here uses (or can use) the mock config and database.
pytestmark = [pytest.mark.usefixtures("mutable_config", "mutable_database")]

path = SpackCommand("path")
location = SpackCommand("location")


@pytest.fixture
def mock_spec():
    # Make it look like the source was actually expanded.
    s = spack.concretize.concretize_one("externaltest")
    source_path = s.package.stage.source_path
    mkdirp(source_path)
    yield s, s.package
    # Remove the spec from the mock stage area.
    shutil.rmtree(s.package.stage.path)


#
# Defaults: this is where `spack path` and `spack location` differ.
#
@pytest.mark.db
@pytest.mark.not_on_windows("Broken on Windows")
def test_path_defaults_to_install_dir(mock_spec):
    """`spack path <spec>` with no options prints the spec's install prefix."""
    spec, _ = mock_spec
    assert path(spec.name).strip() == spec.prefix


@pytest.mark.regression("22738")
def test_location_defaults_to_source_dir(mock_spec):
    """`spack location <spec>` with no options prints the spec's source dir."""
    spec, pkg = mock_spec
    assert location(spec.name).strip() == pkg.stage.source_path


#
# Deprecation: only `spack location` is deprecated, and only its help says so.
#
def test_location_help_is_deprecated():
    assert "deprecated" in location("-h")


def test_path_help_is_not_deprecated():
    assert "deprecated" not in path("-h")


#
# Shared options. These resolve identically for `path` and `location`, so they
# are exercised once, through `spack path`.
#
def test_first(install_mockery, mock_fetch, mock_archive, mock_packages):
    """Test with and without the --first option"""
    install = SpackCommand("install")
    install("--fake", "libelf@0.8.12")
    install("--fake", "libelf@0.8.13")
    # This would normally return an error without --first
    assert path("--first", "--install-dir", "libelf")


@pytest.mark.db
@pytest.mark.not_on_windows("Broken on Windows")
def test_install_dir(mock_spec):
    """Tests spack path --install-dir."""
    spec, _ = mock_spec
    assert path("--install-dir", spec.name).strip() == spec.prefix


def test_build_dir(mock_spec):
    """Tests spack path --build-dir."""
    spec, pkg = mock_spec
    assert path("--build-dir", spec.name).strip() == pkg.stage.source_path


def test_source_dir(mock_spec):
    """Tests spack path --source-dir."""
    spec, pkg = mock_spec
    assert path("--source-dir", spec.name).strip() == pkg.stage.source_path


def test_source_dir_missing():
    """Tests spack path --source-dir with a missing source directory."""
    spec = "mpileaks"
    prefix = "==> Error: "
    expected = (
        "%sSource directory does not exist yet. Run this to create it:"
        "%s  spack stage %s" % (prefix, "\n", spec)
    )
    out = path("--source-dir", spec, fail_on_error=False).strip()
    assert out == expected


@pytest.mark.parametrize(
    "options,expected_code",
    [
        ([], 2),
        (["--source-dir", "mpileaks"], 1),
        (["--env", "missing-env"], 1),
        (["spec1", "spec2"], 2),
    ],
)
def test_cmd_error(options, expected_code):
    """Ensure the proper error is raised with problematic options."""
    with pytest.raises(spack.main.SpackCommandError) as e:
        path(*options)
    assert e.value.code == expected_code


def test_env_exists(mutable_mock_env_path):
    """Tests spack path --env <name> for an existing environment."""
    e = ev.create("example")
    e.write()
    assert path("--env", "example").strip() == e.path


def test_with_active_env(mutable_mock_env_path):
    """Tests spack path --env with active env"""
    e = ev.create("example")
    e.write()
    with e:
        assert path("--env").strip() == e.path


def test_env_missing():
    """Tests spack path --env."""
    missing_env_name = "missing-env"
    error = "==> Error: no such environment: '%s'" % missing_env_name
    out = path("--env", missing_env_name, fail_on_error=False).strip()
    assert out == error


def test_active_view(mutable_mock_env_path, monkeypatch):
    """Tests spack path --view for the active view."""
    mutable_mock_env_path.mkdir()
    view_path = os.path.abspath(mutable_mock_env_path / "path" / "to" / "view")
    spack_yaml = mutable_mock_env_path / ev.manifest_name
    spack_yaml.write_text(
        f"""spack:
      specs: []
      view:
        viewname:
          root: {view_path}
      concretizer:
        unify: True
    """
    )
    e = ev.Environment(mutable_mock_env_path)
    monkeypatch.setenv(ev.spack_env_view_var, "viewname")
    with e:
        assert path("--view").strip() == view_path


def test_no_active_view(mutable_mock_env_path):
    """Tests spack path --env without active view."""
    mutable_mock_env_path.mkdir()
    view_path = os.path.abspath(mutable_mock_env_path / "path" / "to" / "view")
    spack_yaml = mutable_mock_env_path / ev.manifest_name
    spack_yaml.write_text(
        f"""spack:
      specs: []
      view:
        viewname:
          root: {view_path}
      concretizer:
        unify: True
    """
    )
    e = ev.Environment(mutable_mock_env_path)
    error = "==> Error: no active view in the current environment"
    with e:
        out = path("--view", fail_on_error=False).strip()
        assert out == error


def test_view_exists(mutable_mock_env_path):
    """Tests spack path --view <name> for an existing view."""
    mutable_mock_env_path.mkdir()
    view_path = os.path.abspath(mutable_mock_env_path / "path" / "to" / "view")
    spack_yaml = mutable_mock_env_path / ev.manifest_name
    spack_yaml.write_text(
        f"""spack:
      specs: []
      view:
        viewname:
          root: {view_path}
      concretizer:
        unify: True
    """
    )
    e = ev.Environment(mutable_mock_env_path)
    with e:
        assert path("--view", "viewname").strip() == view_path


def test_view_missing(mutable_mock_env_path):
    """Tests spack path --env <view> with missing view."""
    e = ev.create("example", with_view=True)
    e.write()
    missing_view_name = "missing-view"
    error = "==> Error: no such view in the current environment: '%s'" % missing_view_name
    with e:
        out = path("--view", missing_view_name, fail_on_error=False).strip()
        assert out == error


@pytest.mark.db
def test_package_dir(mock_spec):
    """Tests spack path --package-dir."""
    spec, pkg = mock_spec
    assert path("--package-dir", spec.name).strip() == pkg.package_dir


@pytest.mark.db
@pytest.mark.parametrize(
    "option,expected",
    [
        ("--module-dir", spack.paths.module_path),
        ("--packages", spack.paths.mock_packages_path),
        ("--spack-root", spack.paths.prefix),
    ],
)
def test_paths_options(option, expected):
    """Tests basic spack.paths options."""
    assert path(option).strip() == expected


@pytest.mark.parametrize(
    "specs,expected",
    [([], "requires a spec"), (["spec1", "spec2"], "too many specs, supply only one")],
)
def test_spec_errors(specs, expected):
    """Tests spack path with bad spec options."""
    output = path(*specs, fail_on_error=False)
    assert expected in output
    assert path.returncode == 2


@pytest.mark.db
def test_stage_dir(mock_spec):
    """Tests spack path --stage-dir."""
    spec, pkg = mock_spec
    assert path("--stage-dir", spec.name).strip() == pkg.stage.path


@pytest.mark.db
def test_stages(mock_spec):
    """Tests spack path --stages."""
    assert path("--stages").strip() == spack.stage.get_stage_root()


def test_specified_repo():
    """Tests spack path --repo <repo>."""
    with spack.repo.use_repositories(
        os.path.join(spack.paths.test_repos_path, "spack_repo", "builtin_mock"),
        os.path.join(spack.paths.test_repos_path, "spack_repo", "builder_test"),
    ):
        assert path("--repo").strip() == spack.repo.PATH.get_repo("builtin_mock").root
        assert (
            path("--repo", "builtin_mock").strip() == spack.repo.PATH.get_repo("builtin_mock").root
        )
        assert (
            path("--packages", "builder_test").strip()
            == spack.repo.PATH.get_repo("builder_test").root
        )
        assert (
            path("--repo", "nonexistent", fail_on_error=False).strip()
            == "==> Error: no such repository: 'nonexistent'"
        )
