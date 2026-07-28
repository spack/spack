# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import re

import pytest

import spack.cmd
import spack.concretize
import spack.environment as ev
import spack.error
import spack.solver.asp
import spack.spec
from spack.config import Configuration
from spack.main import SpackCommand, SpackCommandError
from spack.store import Store

buildcache = SpackCommand("buildcache")
install = SpackCommand("install")
mirror = SpackCommand("mirror")
uninstall = SpackCommand("uninstall")

# Unit tests should not be affected by the user's managed environments
pytestmark = pytest.mark.usefixtures(
    "mutable_mock_env_path", "mutable_config", "mutable_mock_repo"
)

spec = SpackCommand("spec")


def test_spec():
    output = spec("mpileaks")

    assert "mpileaks@2.3" in output
    assert "callpath@1.0" in output
    assert "dyninst@8.2" in output
    assert "libdwarf@20130729" in output
    assert "libelf@0.8.1" in output
    assert "mpich@3.0.4" in output


def test_spec_concretizer_args(mutable_database):
    """End-to-end test of CLI concretizer prefs.

    It's here to make sure that everything works from CLI
    options to `solver.py`, and that config options are not
    lost along the way.
    """
    # remove two non-preferred mpileaks installations
    # so that reuse will pick up the zmpi one
    uninstall = SpackCommand("uninstall")
    uninstall("-y", "mpileaks^mpich")
    uninstall("-y", "mpileaks^mpich2")

    # get the hash of mpileaks^zmpi
    mpileaks_zmpi = mutable_database.query_one("mpileaks^zmpi")
    h = mpileaks_zmpi.dag_hash()[:7]

    output = spec("--fresh", "-l", "mpileaks")
    assert h not in output

    output = spec("--reuse", "-l", "mpileaks")
    assert h in output


def test_spec_parse_dependency_variant_value():
    """Verify that we can provide multiple key=value variants to multiple separate
    packages within a spec string."""
    output = spec("multivalue-variant fee=barbaz ^ pkg-a foobar=baz")

    assert "fee=barbaz" in output
    assert "foobar=baz" in output


def test_spec_parse_cflags_quoting():
    """Verify that compiler flags can be provided to a spec from the command line."""
    output = spec("--yaml", 'gcc cflags="-Os -pipe" cxxflags="-flto -Os"')
    gh_flagged = spack.spec.Spec.from_yaml(output)

    assert ["-Os", "-pipe"] == gh_flagged.compiler_flags["cflags"]
    assert ["-flto", "-Os"] == gh_flagged.compiler_flags["cxxflags"]


def test_spec_yaml():
    output = spec("--yaml", "mpileaks")

    mpileaks = spack.spec.Spec.from_yaml(output)
    assert "mpileaks" in mpileaks
    assert "callpath" in mpileaks
    assert "dyninst" in mpileaks
    assert "libdwarf" in mpileaks
    assert "libelf" in mpileaks
    assert "mpich" in mpileaks


def test_spec_json():
    output = spec("--json", "mpileaks")

    mpileaks = spack.spec.Spec.from_json(output)
    assert "mpileaks" in mpileaks
    assert "callpath" in mpileaks
    assert "dyninst" in mpileaks
    assert "libdwarf" in mpileaks
    assert "libelf" in mpileaks
    assert "mpich" in mpileaks


def test_spec_format(mutable_database):
    output = spec("--format", "{name}-{^mpi.name}", "mpileaks^mpich")
    print(output)
    assert output.rstrip("\n") == "mpileaks-mpich"


def _parse_types(string):
    """Parse deptypes for specs from `spack spec -t` output."""
    lines = string.strip().split("\n")

    result = {}
    for line in lines:
        match = re.match(r"\[([^]]*)\]\s*\^?([^@]*)@", line)
        if match:
            types, name = match.groups()
            result.setdefault(name, []).append(types)
            result[name] = sorted(result[name])
    return result


def test_spec_deptypes_nodes():
    output = spec("--types", "--cover", "nodes", "--no-install-status", "dt-diamond")
    types = _parse_types(output)

    assert types["dt-diamond"] == ["    "]
    assert types["dt-diamond-left"] == ["bl  "]
    assert types["dt-diamond-right"] == ["bl  "]
    assert types["dt-diamond-bottom"] == ["blr "]


def test_spec_deptypes_edges():
    output = spec("--types", "--cover", "edges", "--no-install-status", "dt-diamond")
    types = _parse_types(output)

    assert types["dt-diamond"] == ["    "]
    assert types["dt-diamond-left"] == ["bl  "]
    assert types["dt-diamond-right"] == ["bl  "]
    assert types["dt-diamond-bottom"] == ["b   ", "blr "]


def test_spec_returncode():
    with pytest.raises(SpackCommandError):
        spec()
    assert spec.returncode == 2


def test_spec_parse_error():
    with pytest.raises(spack.error.SpecSyntaxError) as e:
        spec("1.15:")

    # make sure the error is formatted properly
    error_msg = "unexpected characters in the spec string\n1.15:\n    ^"
    assert error_msg in str(e.value)


def test_env_aware_spec(mutable_mock_env_path):
    env = ev.create("test")
    env.add("mpileaks")

    with env:
        output = spec()
        assert "mpileaks@2.3" in output
        assert "callpath@1.0" in output
        assert "dyninst@8.2" in output
        assert "libdwarf@20130729" in output
        assert "libelf@0.8.1" in output
        assert "mpich@3.0.4" in output


def _concretize_and_lock(env: ev.Environment) -> None:
    with env:
        env.concretize()
        env.write()


@pytest.mark.parametrize("unify", [True, False, "when_possible"])
def test_spec_does_not_reconcretize_concrete_env(
    unify, mutable_mock_env_path, mutable_config: Configuration
):
    """A concrete environment's roots must be shown as-is, even if a fresh solve
    would pick something different (regression for spack/spack#...)."""
    mutable_config.set("concretizer:unify", unify)
    env = ev.create("test")
    env.add("mpileaks")
    _concretize_and_lock(env)
    locked_hashes = {s.dag_hash() for s in env.concrete_roots()}

    # A fresh solve would now pick a different mpileaks version
    mutable_config.set("packages", {"mpileaks": {"require": ["@2.2"]}})

    with env:
        output = spec("-l")
    assert "mpileaks@2.3" in output
    assert any(h[:7] in output for h in locked_hashes)
    assert "mpileaks@2.2" not in output


def test_spec_env_force_reconcretizes_without_modifying(
    mutable_mock_env_path, mutable_config: Configuration
):
    """--force shows a full re-solve, but the environment is not modified."""
    env = ev.create("test")
    env.add("mpileaks")
    _concretize_and_lock(env)
    lock_content = env.lock_path and open(env.lock_path).read()

    mutable_config.set("packages", {"mpileaks": {"require": ["@2.2"]}})

    with env:
        output = spec("--force")
    assert "mpileaks@2.2" in output

    # neither the in-memory state nor the lockfile changed
    reread = ev.Environment(env.path)
    assert {s.dag_hash() for s in reread.concrete_roots()} == {
        s.dag_hash() for s in env.concrete_roots()
    }
    assert open(env.lock_path).read() == lock_content
    assert any(s.satisfies("mpileaks@2.3") for s in env.concrete_roots())


@pytest.mark.parametrize("unify", [True, False, "when_possible"])
def test_spec_env_concretizes_only_new_specs(
    unify, mutable_mock_env_path, mutable_config: Configuration
):
    """Only not-yet-concrete user specs are solved; kept roots are not changed, and
    the environment is not modified."""
    mutable_config.set("concretizer:unify", unify)
    env = ev.create("test")
    env.add("mpileaks")
    _concretize_and_lock(env)
    mpileaks_hash = next(iter(s.dag_hash() for s in env.concrete_roots()))
    lock_content = open(env.lock_path).read()

    # A fresh solve of mpileaks would now pick 2.2: proof it isn't re-solved
    mutable_config.set("packages", {"mpileaks": {"version": ["2.2"]}})

    with env:
        env.add("libelf")
        output = spec("-l")

    assert "libelf" in output
    assert "mpileaks@2.3" in output
    assert mpileaks_hash[:7] in output

    # the new root was not committed to the environment
    reread = ev.Environment(env.path)
    assert {s.name for s in reread.concrete_roots()} == {"mpileaks"}
    assert open(env.lock_path).read() == lock_content


def test_spec_env_fully_concrete_skips_solver(mutable_mock_env_path, monkeypatch):
    """Displaying a fully concrete environment must not invoke the solver."""
    env = ev.create("test")
    env.add("mpileaks")
    _concretize_and_lock(env)

    def no_solve(*args, **kwargs):
        raise AssertionError("solver should not run for a fully concrete environment")

    monkeypatch.setattr(spack.solver.asp.PyclingoDriver, "solve", no_solve)
    with env:
        output = spec()
    assert "mpileaks@2.3" in output


def test_spec_env_show_opt_reports_fully_concrete(mutable_mock_env_path):
    """--show opt on a fully concrete environment explains there is nothing to solve."""
    env = ev.create("test")
    env.add("mpileaks")
    _concretize_and_lock(env)

    with env:
        output = spec("--show", "opt")
    assert "already concrete" in output
    assert "Priority" not in output


@pytest.mark.parametrize("unify", [True, False, "when_possible"])
def test_spec_env_show_opt_for_new_specs(
    unify, mutable_mock_env_path, mutable_config: Configuration
):
    """--show opt prints optimization criteria for the newly solved portion."""
    mutable_config.set("concretizer:unify", unify)
    env = ev.create("test")
    env.add("mpileaks")
    _concretize_and_lock(env)

    with env:
        env.add("libelf")
        output = spec("--show", "opt")
    assert "Priority" in output
    assert "considered solutions" in output


def test_spec_env_show_asp(mutable_mock_env_path):
    """--show asp prints the ASP program for the new solve, without concretizing."""
    env = ev.create("test")
    env.add("mpileaks")
    _concretize_and_lock(env)
    lock_content = open(env.lock_path).read()

    with env:
        env.add("libelf")
        output = spec("--show", "asp")
    assert "Target Constraints" in output
    assert open(env.lock_path).read() == lock_content


def test_spec_env_diagnostics_per_spec_blocks(
    mutable_mock_env_path, mutable_config: Configuration
):
    """With unify:false, each newly solved spec gets its own labeled diagnostics block."""
    mutable_config.set("concretizer:unify", False)
    env = ev.create("test")
    env.add("mpileaks")
    _concretize_and_lock(env)

    with env:
        env.add("libelf")
        env.add("libdwarf")
        output = spec("--show", "opt")

    blocks = re.findall(r"Solve diagnostics for (\S+)", output)
    assert sorted(blocks) == ["libdwarf", "libelf"]
    assert output.count("considered solutions") == 2


@pytest.mark.parametrize(
    "name, version, error",
    [
        ("develop-branch-version", "f3c7206350ac8ee364af687deaae5c574dcfca2c=develop", None),
        ("develop-branch-version", "git." + "a" * 40 + "=develop", None),
        ("callpath", "f3c7206350ac8ee364af687deaae5c574dcfca2c=1.0", spack.error.PackageError),
        ("develop-branch-version", "git.foo=0.2.15", None),
    ],
)
@pytest.mark.use_package_hash
def test_spec_version_assigned_git_ref_as_version(name, version, error):
    if error:
        with pytest.raises(error):
            output = spec(name + "@" + version)
    else:
        output = spec(name + "@" + version)
        assert version in output


@pytest.mark.parametrize(
    "unify, spec_hash_args, match, error",
    [
        # success cases with unfiy:true
        (True, ["mpileaks_mpich"], "mpich", None),
        (True, ["mpileaks_zmpi"], "zmpi", None),
        (True, ["mpileaks_mpich", "dyninst"], "mpich", None),
        (True, ["mpileaks_zmpi", "dyninst"], "zmpi", None),
        # same success cases with unfiy:false
        (False, ["mpileaks_mpich"], "mpich", None),
        (False, ["mpileaks_zmpi"], "zmpi", None),
        (False, ["mpileaks_mpich", "dyninst"], "mpich", None),
        (False, ["mpileaks_zmpi", "dyninst"], "zmpi", None),
        # cases with unfiy:false
        (True, ["mpileaks_mpich", "mpileaks_zmpi"], "mpileaks.*, mpileaks", spack.error.SpecError),
        (False, ["mpileaks_mpich", "mpileaks_zmpi"], "zmpi", None),
    ],
)
def test_spec_unification_from_cli(
    install_mockery,
    mutable_config: Configuration,
    mutable_database,
    unify,
    spec_hash_args,
    match,
    error,
):
    """Ensure specs grouped together on the CLI are concretized together when unify:true."""
    mutable_config.set("concretizer:unify", unify)

    db = mutable_database
    spec_lookup = {
        "mpileaks_mpich": db.query_one("mpileaks ^mpich").dag_hash(),
        "mpileaks_zmpi": db.query_one("mpileaks ^zmpi").dag_hash(),
        "dyninst": db.query_one("dyninst").dag_hash(),
    }

    hashes = [f"/{spec_lookup[name]}" for name in spec_hash_args]
    if error:
        with pytest.raises(error, match=match):
            output = spec(*hashes)
    else:
        output = spec(*hashes)
        assert match in output


def test_buildcache_status_fn_marks_absent_spec(
    temporary_store: Store, install_mockery, mock_packages
):
    """Tests the basic semantics of build_cache_status_fn."""
    s = spack.concretize.concretize_one("mpileaks")
    assert temporary_store.db.install_status(s) == spack.spec.InstallStatus.absent

    status_fn = spack.cmd.buildcache_status_fn({s.dag_hash()})
    assert status_fn(s) == spack.spec.InstallStatus.buildcache

    status_fn = spack.cmd.buildcache_status_fn(set())
    assert status_fn(s) == spack.spec.InstallStatus.absent


def test_buildcache_status_fn_installed_not_overridden(mutable_database):
    """Tests that an installed spec stays installed even if its hash is in the cache."""
    s = mutable_database.query_one("mpileaks^mpich")
    assert mutable_database.install_status(s) == spack.spec.InstallStatus.installed

    status_fn = spack.cmd.buildcache_status_fn({s.dag_hash()})
    assert status_fn(s) == spack.spec.InstallStatus.installed
