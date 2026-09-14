# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
import io
import pathlib

import pytest

import spack.environment as ev
import spack.error
import spack.repo
from spack.cmd import (
    CommandNameError,
    PythonNameError,
    cmd_name,
    matching_specs_from_env,
    parse_specs,
    python_name,
    report_unknown_package,
    require_cmd_name,
    require_python_name,
)
from spack.config import Configuration
from spack.database import Database
from spack.solver import asp


def test_require_python_name():
    """Python module names should not contain dashes---ensure that
    require_python_name() raises the appropriate exception if one is
    detected.
    """
    require_python_name("okey_dokey")
    with pytest.raises(PythonNameError):
        require_python_name("okey-dokey")
    require_python_name(python_name("okey-dokey"))


def test_require_cmd_name():
    """By convention, Spack command names should contain dashes rather than
    underscores---ensure that require_cmd_name() raises the appropriate
    exception if underscores are detected.
    """
    require_cmd_name("okey-dokey")
    with pytest.raises(CommandNameError):
        require_cmd_name("okey_dokey")
    require_cmd_name(cmd_name("okey_dokey"))


@pytest.mark.parametrize(
    "unify,spec_strs,error",
    [
        # single spec
        (True, ["zmpi"], None),
        (False, ["mpileaks"], None),
        # multiple specs, some from hash some from file
        (True, ["zmpi", "mpileaks^zmpi", "libelf"], None),
        (True, ["mpileaks^zmpi", "mpileaks^mpich", "libelf"], spack.error.SpecError),
        (False, ["mpileaks^zmpi", "mpileaks^mpich", "libelf"], None),
    ],
)
def test_special_cases_concretization_parse_specs(
    unify,
    spec_strs,
    error,
    monkeypatch,
    mutable_config: Configuration,
    mutable_database: Database,
    tmp_path: pathlib.Path,
):
    """Test that special cases in parse_specs(concretize=True) bypass solver"""

    # monkeypatch to ensure we do not call the actual concretizer
    def _fail(*args, **kwargs):
        assert False

    monkeypatch.setattr(asp.SpackSolverSetup, "setup", _fail)

    mutable_config.set("concretizer:unify", unify)

    args = [f"/{mutable_database.query(s)[0].dag_hash()}" for s in spec_strs]
    if len(args) > 1:
        # We convert the last one to a specfile input
        filename = tmp_path / "spec.json"
        spec = parse_specs(args[-1], concretize=True)[0]
        with open(filename, "w", encoding="utf-8") as f:
            spec.to_json(f)
        args[-1] = str(filename)

    if error:
        with pytest.raises(error):
            parse_specs(args, concretize=True)
    else:
        # assertion error from monkeypatch above if test fails
        parse_specs(args, concretize=True)


@pytest.mark.parametrize(
    "unify,spec_strs,error",
    [
        # single spec
        (True, ["zmpi"], None),
        (False, ["mpileaks"], None),
        # multiple specs, some from hash some from file
        (True, ["zmpi", "mpileaks^zmpi", "libelf"], None),
        (True, ["mpileaks^zmpi", "mpileaks^mpich", "libelf"], spack.error.SpecError),
        (False, ["mpileaks^zmpi", "mpileaks^mpich", "libelf"], None),
    ],
)
def test_special_cases_concretization_matching_specs_from_env(
    unify,
    spec_strs,
    error,
    monkeypatch,
    mutable_config: Configuration,
    mutable_database: Database,
    tmp_path: pathlib.Path,
    mutable_mock_env_path,
):
    """Test that special cases in parse_specs(concretize=True) bypass solver"""

    # monkeypatch to ensure we do not call the actual concretizer
    def _fail(*args, **kwargs):
        assert False

    monkeypatch.setattr(asp.SpackSolverSetup, "setup", _fail)

    mutable_config.set("concretizer:unify", unify)

    ev.create("test")
    env = ev.read("test")

    args = [f"/{mutable_database.query(s)[0].dag_hash()}" for s in spec_strs]
    if len(args) > 1:
        # We convert the last one to a specfile input
        filename = tmp_path / "spec.json"
        spec = parse_specs(args[-1], concretize=True)[0]
        with open(filename, "w", encoding="utf-8") as f:
            spec.to_json(f)
        args[-1] = str(filename)

    with env:
        specs = parse_specs(args, concretize=False)
        if error:
            with pytest.raises(error):
                matching_specs_from_env(specs)
        else:
            # assertion error from monkeypatch above if test fails
            matching_specs_from_env(specs)


def test_report_unknown_package_suggests(mock_packages):
    """A misspelled name is reported with the packages it is close to."""
    out = io.StringIO()
    report_unknown_package(spack.repo.UnknownPackageError("mpileak"), repo=mock_packages, out=out)
    assert "Package 'mpileak' not found" in out.getvalue()
    assert "mpileaks" in out.getvalue()


def test_report_unknown_package_hint(mock_packages):
    """Advice beyond the name comes from the command that caught the error."""
    error = spack.repo.UnknownPackageError("mpileak")

    out = io.StringIO()
    report_unknown_package(error, repo=mock_packages, out=out)
    assert "spack create" not in out.getvalue()

    out = io.StringIO()
    report_unknown_package(error, hint="Use 'spack create'.", repo=mock_packages, out=out)
    assert "Use 'spack create'." in out.getvalue()


def test_report_unknown_package_anonymous(mock_packages):
    """An error without a name does not suggest a name."""
    out = io.StringIO()
    report_unknown_package(spack.repo.UnknownPackageError(None), repo=mock_packages, out=out)
    assert "Did you mean" not in out.getvalue()


def test_parse_specs_rejects_unknown_names(mock_packages):
    """An unknown name is rejected before concretization."""
    with pytest.raises(spack.repo.UnknownPackageError) as exc_info:
        parse_specs(["mpileak"], concretize=True)
    assert exc_info.value.name == "mpileak"


def test_parse_specs_keeps_the_filename_hint(mock_packages):
    """A namespace that is not configured is reported as such, so the hint survives."""
    with pytest.raises(spack.repo.UnknownNamespaceError) as exc_info:
        parse_specs(["libelf.yaml"], concretize=True)

    out = io.StringIO()
    report_unknown_package(exc_info.value, out=out)
    assert "./libelf.yaml" in out.getvalue()
