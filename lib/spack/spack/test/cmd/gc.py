# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


import pytest

import spack.environment as ev
import spack.main
import spack.spec

gc = spack.main.SpackCommand("gc")
add = spack.main.SpackCommand("add")
install = spack.main.SpackCommand("install")

pytestmark = pytest.mark.not_on_windows("does not run on windows")


@pytest.mark.db
def test_gc_without_build_dependency(config, mutable_database):
    output = gc("-yb")
    assert "There are no unused specs." in output

    output = gc("-y")
    assert "There are no unused specs." in output


@pytest.mark.db
def test_gc_with_build_dependency(config, mutable_database):
    s = spack.spec.Spec("simple-inheritance")
    s.concretize()
    s.package.do_install(fake=True, explicit=True)

    output = gc("-yb")
    assert "There are no unused specs." in output

    output = gc("-y")
    assert "Successfully uninstalled cmake" in output


@pytest.mark.db
def test_gc_with_environment(config, mutable_database, mutable_mock_env_path):
    s = spack.spec.Spec("simple-inheritance")
    s.concretize()
    s.package.do_install(fake=True, explicit=True)

    e = ev.create("test_gc")
    with e:
        add("cmake")
        install()
        assert mutable_database.query_local("cmake")
        output = gc("-y")
    assert "Restricting garbage collection" in output
    assert "There are no unused specs" in output


@pytest.mark.db
def test_gc_with_build_dependency_in_environment(config, mutable_database, mutable_mock_env_path):
    s = spack.spec.Spec("simple-inheritance")
    s.concretize()
    s.package.do_install(fake=True, explicit=True)

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
        output = gc("-y")
    assert "Restricting garbage collection" in output
    assert "Successfully uninstalled cmake" in output


@pytest.mark.db
def test_gc_except_any_environments(config, mutable_database, mutable_mock_env_path):
    s = spack.spec.Spec("simple-inheritance")
    s.concretize()
    s.package.do_install(fake=True, explicit=True)

    assert mutable_database.query_local("zmpi")

    e = ev.create("test_gc")
    with e:
        add("simple-inheritance")
        install()
        assert mutable_database.query_local("simple-inheritance")

    output = gc("-yE")
    assert "Restricting garbage collection" not in output
    assert "Successfully uninstalled zmpi" in output
    assert not mutable_database.query_local("zmpi")

    with e:
        output = gc("-yE")
    assert "Restricting garbage collection" not in output
    assert "There are no unused specs" not in output


@pytest.mark.db
def test_gc_except_specific_environments(config, mutable_database, mutable_mock_env_path):
    s = spack.spec.Spec("simple-inheritance")
    s.concretize()
    s.package.do_install(fake=True, explicit=True)

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
def test_gc_except_nonexisting_dir_env(config, mutable_database, mutable_mock_env_path, tmpdir):
    output = gc("-ye", tmpdir.strpath, fail_on_error=False)
    assert "No such environment" in output
    gc.returncode == 1


@pytest.mark.db
def test_gc_except_specific_dir_env(config, mutable_database, mutable_mock_env_path, tmpdir):
    s = spack.spec.Spec("simple-inheritance")
    s.concretize()
    s.package.do_install(fake=True, explicit=True)

    assert mutable_database.query_local("zmpi")

    e = ev.create_in_dir(tmpdir.strpath)
    with e:
        add("simple-inheritance")
        install()
        assert mutable_database.query_local("simple-inheritance")

    output = gc("-ye", tmpdir.strpath)
    assert "Restricting garbage collection" not in output
    assert "Successfully uninstalled zmpi" in output
    assert not mutable_database.query_local("zmpi")
