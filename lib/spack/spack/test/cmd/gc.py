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
import spack.store
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


@pytest.mark.db
def test_gc_drop_group(install_mockery, mock_fetch, mutable_mock_env_path, tmp_path: pathlib.Path):
    """Tests that --drop-group removes the roots of the dropped group and their unique deps."""
    spack_yaml = tmp_path / "spack.yaml"
    spack_yaml.write_text(
        """\
spack:
  specs:
  - group: tools
    specs:
    - cmake
  - group: apps
    specs:
    - libelf
"""
    )
    e = ev.create("test_gc_drop_group", init_file=str(spack_yaml))
    with e:
        e.concretize()
        e.install_all(fake=True)
        e.write()
        output = gc("-y", "--drop-group", "tools")

    assert "Restricting garbage collection" in output
    assert "Successfully uninstalled cmake" in output
    assert not spack.store.STORE.db.query_local("cmake")
    assert spack.store.STORE.db.query_local("libelf")


@pytest.mark.db
def test_gc_drop_group_requires_active_env(mutable_database):
    """Tests that --drop-group fails without an active environment."""
    output = gc("--drop-group", "tools", fail_on_error=False)
    assert gc.returncode == 1
    assert "--drop-group requires an active environment" in output


@pytest.mark.db
def test_gc_drop_group_unknown_group(mutable_mock_env_path):
    """Tests that --drop-group fails when the group is not defined in the environment."""
    e = ev.create("test_gc_bad_group")
    with e:
        add("cmake")
        output = gc("--drop-group", "nonexistent", fail_on_error=False)
    assert gc.returncode == 1
    assert "nonexistent" in output


@pytest.mark.db
def test_gc_drop_group_incompatible_with_e(mutable_database, mutable_mock_env_path):
    """Tests that --drop-group cannot be combined with -e."""
    e = ev.create("test_gc_compat")
    with e:
        output = gc("--drop-group", "tools", "-e", "test_gc_compat", fail_on_error=False)
    assert gc.returncode == 1
    assert "--drop-group cannot be combined" in output
