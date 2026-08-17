# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import json
import pathlib
import re
from typing import List

import pytest

import spack.cmd
import spack.concretize
import spack.environment as ev
import spack.error
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
        (True, ["mpileaks_mpich", "mpileaks_zmpi"], "callpath, mpileaks", spack.error.SpecError),
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


def _roots() -> List[spack.spec.Spec]:
    """Returns the concrete roots that `spack spec` reports, sorted by name."""
    data = [json.loads(x) for x in spec("--json").splitlines() if x.strip()]
    return sorted((spack.spec.Spec.from_dict(x) for x in data), key=lambda x: x.name)


def _root_names() -> List[str]:
    return [x.name for x in _roots()]


@pytest.mark.parametrize("unify", ["true", "false", "when_possible"])
def test_spec_in_empty_environment(tmp_path: pathlib.Path, unify):
    """Tests that an empty environment doesn't fail with `spack spec`."""
    (tmp_path / ev.manifest_name).write_text(
        f"""\
spack:
  concretizer:
    unify: {unify}
  specs: []
"""
    )
    with ev.Environment(tmp_path):
        assert _root_names() == []


@pytest.mark.parametrize("unify", ["true", "false", "when_possible"])
@pytest.mark.parametrize(
    "expected,spack_yaml",
    [
        (
            ["libelf"],
            """\
spack:
  concretizer:
    unify: {unify}
  specs:
  - group: tools
    specs:
    - libelf
""",
        ),
        (
            ["libelf", "mpich"],
            """\
spack:
  concretizer:
    unify: {unify}
  specs:
  - mpich
  - group: tools
    specs:
    - libelf
""",
        ),
    ],
)
def test_spec_env_with_groups_only(unify, tmp_path: pathlib.Path, spack_yaml, expected):
    """Tests that `spack spec` uses the root specs of every group, not just the default one."""
    (tmp_path / ev.manifest_name).write_text(spack_yaml.format(unify=unify))
    with ev.Environment(tmp_path):
        assert _root_names() == expected


def test_spec_env_applies_group_config_override(tmp_path: pathlib.Path):
    """Tests that the "override" scope of a group is active while solving that group."""
    (tmp_path / ev.manifest_name).write_text(
        """\
spack:
  specs:
  - group: pinned
    override:
      packages:
        libelf:
          require: "@0.8.12"
    specs:
    - libelf
"""
    )
    with ev.Environment(tmp_path):
        roots = _roots()

    assert len(roots) == 1
    assert roots[0].satisfies("libelf@0.8.12")


def test_spec_env_reuses_specs_from_needed_groups(tmp_path: pathlib.Path):
    """Tests that specs from a group listed in "needs" are reused."""
    (tmp_path / ev.manifest_name).write_text(
        """\
spack:
  concretizer:
    unify: true
    reuse: false
  specs:
  - group: compiler
    override:
      packages:
        gcc:
          require: "@12.1.0"
    specs:
    - gcc
  - group: apps
    needs: [compiler]
    specs:
    - mpileaks
"""
    )
    with ev.Environment(tmp_path) as env:
        # Ground truth: this is what `spack install` would build
        env.concretize()
        _, gcc = next(iter(env.concretized_specs_by(group="compiler")))
        _, mpileaks = next(iter(env.concretized_specs_by(group="apps")))
        assert mpileaks["c"].dag_hash() == gcc.dag_hash()

    # The environment on disk is still not concretized, so `spack spec` has to solve it
    with ev.Environment(tmp_path):
        reported = _roots()

    # Concrete specs compare by DAG hash, so this checks the whole sub-DAG of each root
    assert reported == [gcc, mpileaks]


def test_spec_env_reports_the_concretized_state(tmp_path: pathlib.Path, mutable_config):
    """Tests that in a concretized environment `spack spec` reports what is in the lockfile."""
    (tmp_path / ev.manifest_name).write_text(
        """\
spack:
  specs:
  - libelf
"""
    )
    mutable_config.set("packages:libelf:require", "@0.8.12")
    with ev.Environment(tmp_path) as env:
        env.concretize()
        env.write()

    # Configuration drifts after the environment has been concretized
    mutable_config.set("packages:libelf:require", "@0.8.13")
    with ev.Environment(tmp_path):
        roots = _roots()

    assert len(roots) == 1
    assert roots[0].satisfies("libelf@0.8.12")


def test_spec_env_reports_included_concrete_roots(tmp_path: pathlib.Path):
    """Tests that roots coming from an included concrete environment are reported too."""
    include_dir = tmp_path / "included"
    include_dir.mkdir()
    (include_dir / ev.manifest_name).write_text(
        """\
spack:
  specs:
  - libelf
"""
    )
    included = ev.Environment(include_dir)
    included.concretize()
    included.write()

    root_dir = tmp_path / "root"
    root_dir.mkdir()
    (root_dir / ev.manifest_name).write_text(
        f"""\
spack:
  include:
  - {included.lock_path}
  specs:
  - mpich
"""
    )
    with ev.Environment(root_dir):
        assert _root_names() == ["libelf", "mpich"]


def test_spec_json_output_is_jsonl(mutable_config):
    """Tests that `spack spec --json` emits JSON Lines."""
    mutable_config.set("concretizer:unify", True)
    lines = [x for x in spec("--json", "libelf", "mpich").splitlines() if x.strip()]

    assert len(lines) == 2
    assert {spack.spec.Spec.from_dict(json.loads(x)).name for x in lines} == {"libelf", "mpich"}
