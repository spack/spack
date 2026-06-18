# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import pathlib

import pytest

import spack.concretize
import spack.deptypes as dt
import spack.environment as ev
import spack.main
import spack.spec
import spack.traverse
from spack.installer import PackageInstaller

gc = spack.main.SpackCommand("gc")
add = spack.main.SpackCommand("add")
install = spack.main.SpackCommand("install")


@pytest.mark.db
def test_gc_without_build_dependency(mutable_database):
    assert "There are no unused specs." in gc("-yb")
    # 'gcc' is a pure build dependency in the DB
    assert "There are no unused specs." not in gc("-y")


@pytest.mark.db
def test_gc_with_build_dependency(mutable_database):
    s = spack.concretize.concretize_one("simple-inheritance")
    PackageInstaller([s.package], explicit=True, fake=True).install()

    assert "There are no unused specs." in gc("-yb")
    assert "Successfully uninstalled cmake" in gc("-y")
    assert "There are no unused specs." in gc("-y")


@pytest.mark.db
def test_gc_with_constraints(mutable_database):
    s_cmake1 = spack.concretize.concretize_one("simple-inheritance ^cmake@3.4.3")
    s_cmake2 = spack.concretize.concretize_one("simple-inheritance ^cmake@3.23.1")
    PackageInstaller([s_cmake1.package], explicit=True, fake=True).install()
    PackageInstaller([s_cmake2.package], explicit=True, fake=True).install()

    assert "There are no unused specs." in gc("python")

    assert "Successfully uninstalled cmake@3.4.3" in gc("-y", "cmake@3.4.3")
    assert "There are no unused specs." in gc("-y", "cmake@3.4.3")

    assert "Successfully uninstalled cmake" in gc("-y", "cmake@3.23.1")
    assert "There are no unused specs." in gc("-y", "cmake")


@pytest.mark.db
def test_gc_with_environment(mutable_database, mutable_mock_env_path):
    s = spack.concretize.concretize_one("simple-inheritance")
    PackageInstaller([s.package], explicit=True, fake=True).install()

    e = ev.create("test_gc")
    with e:
        add("cmake")
        install()
        assert mutable_database.query_local("cmake")
        output = gc("-by")
    assert "Restricting garbage collection" in output
    assert "There are no unused specs" in output


@pytest.mark.db
def test_gc_with_build_dependency_in_environment(mutable_database, mutable_mock_env_path):
    s = spack.concretize.concretize_one("simple-inheritance")
    PackageInstaller([s.package], explicit=True, fake=True).install()

    e = ev.create("test_gc")
    with e:
        add("simple-inheritance")
        install()
        assert mutable_database.query_local("simple-inheritance")
        output = gc("-yb")
    assert "Restricting garbage collection" in output
    assert "There are no unused specs" in output

    with e:
        assert mutable_database.query_local("simple-inheritance")
        fst = gc("-y")
        assert "Restricting garbage collection" in fst
        assert "Successfully uninstalled cmake" in fst
        snd = gc("-y")
        assert "Restricting garbage collection" in snd
        assert "There are no unused specs" in snd


@pytest.mark.db
def test_gc_except_any_environments(mutable_database, mutable_mock_env_path):
    """Tests whether the garbage collector can remove all specs except those still needed in some
    environment (needed in the sense of roots + link/run deps)."""
    assert mutable_database.query_local("zmpi")

    e = ev.create("test_gc")
    e.add("simple-inheritance")
    e.concretize()
    e.install_all(fake=True)
    e.write()

    assert mutable_database.query_local("simple-inheritance")
    assert not e.all_matching_specs(spack.spec.Spec("zmpi"))

    output = gc("-yE")
    assert "Restricting garbage collection" not in output
    assert "Successfully uninstalled zmpi" in output
    assert not mutable_database.query_local("zmpi")

    # All runtime specs in this env should still be installed.
    assert all(
        s.installed
        for s in spack.traverse.traverse_nodes(e.concrete_roots(), deptype=dt.LINK | dt.RUN)
    )


@pytest.mark.db
def test_gc_except_specific_environments(mutable_database, mutable_mock_env_path):
    s = spack.concretize.concretize_one("simple-inheritance")
    PackageInstaller([s.package], explicit=True, fake=True).install()

    assert mutable_database.query_local("zmpi")

    e = ev.create("test_gc")
    with e:
        add("simple-inheritance")
        install()
        assert mutable_database.query_local("simple-inheritance")

    output = gc("-ye", "test_gc")
    assert "Restricting garbage collection" not in output
    assert "Successfully uninstalled zmpi" in output
    assert not mutable_database.query_local("zmpi")


@pytest.mark.db
def test_gc_except_nonexisting_dir_env(
    mutable_database, mutable_mock_env_path, tmp_path: pathlib.Path
):
    output = gc("-ye", str(tmp_path), fail_on_error=False)
    assert "No such environment" in output
    assert gc.returncode == 1


@pytest.mark.db
def test_gc_except_specific_dir_env(
    mutable_database, mutable_mock_env_path, tmp_path: pathlib.Path
):
    s = spack.concretize.concretize_one("simple-inheritance")
    PackageInstaller([s.package], explicit=True, fake=True).install()

    assert mutable_database.query_local("zmpi")

    e = ev.create_in_dir(str(tmp_path))
    with e:
        add("simple-inheritance")
        install()
        assert mutable_database.query_local("simple-inheritance")

    output = gc("-ye", str(tmp_path))
    assert "Restricting garbage collection" not in output
    assert "Successfully uninstalled zmpi" in output
    assert not mutable_database.query_local("zmpi")


@pytest.fixture
def mock_installed_environment(mutable_database, mutable_mock_env_path):

    def _create_environment(name, spack_yaml):
        tmp_env = ev.create(name)
        spack_yaml_path = pathlib.Path(tmp_env.path) / "spack.yaml"
        spack_yaml_path.write_text(spack_yaml)
        e = ev.read(name)
        with ev.read(name):
            e.concretize()
            e.install_all(fake=True)
            e.write()
        return e

    return _create_environment


@pytest.mark.db
@pytest.mark.parametrize(
    "explicit,expected_explicit,expected_implicit",
    [
        (True, ["gcc@14.0.1", "openblas", "dyninst"], []),
        (False, ["dyninst"], ["gcc@14.0.1", "openblas"]),
    ],
)
def test_gc_with_explicit_groups(
    explicit, expected_explicit, expected_implicit, mutable_database, mock_installed_environment
):
    """Tests the semantics of the "explicit" attribute of environment groups"""
    e = mock_installed_environment(
        "test_gc_explicit",
        f"""
spack:
  config:
    installer: new
  specs:
  - group: base
    explicit: {explicit}
    specs:
    - gcc@14.0.1
    - openblas
  - group: apps
    needs: [base]
    specs:
    - dyninst %c=gcc@14.0.1
""",
    )

    # Test DB status
    for query in expected_explicit:
        assert mutable_database.query_local(query, explicit=True)

    for query in expected_implicit:
        assert mutable_database.query_local(query, explicit=False)

    with e:
        output = gc("-y")

    # Test gc behavior
    for query in expected_implicit:
        assert f"Successfully uninstalled {query}" in output

    for query in expected_explicit:
        assert f"Successfully uninstalled {query}" not in output
