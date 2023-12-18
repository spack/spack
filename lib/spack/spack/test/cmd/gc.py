# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
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
find = spack.main.SpackCommand("find")

pytestmark = pytest.mark.not_on_windows("does not run on windows")


@pytest.mark.db
def test_gc_without_build_dependency(config, mutable_database, capsys):
    with capsys.disabled():
        output = gc("-yb")
    assert "There are no unused specs." in output

    with capsys.disabled():
        output = gc("-y")
    assert "There are no unused specs." in output


@pytest.mark.db
def test_gc_with_build_dependency(config, mutable_database, capsys):
    s = spack.spec.Spec("simple-inheritance")
    s.concretize()
    s.package.do_install(fake=True, explicit=True)

    with capsys.disabled():
        output = gc("-yb")
    assert "There are no unused specs." in output

    with capsys.disabled():
        output = gc("-y")
    assert "Successfully uninstalled cmake" in output


@pytest.mark.db
def test_gc_with_environment(config, mutable_database, mutable_mock_env_path, capsys):
    s = spack.spec.Spec("simple-inheritance")
    s.concretize()
    s.package.do_install(fake=True, explicit=True)

    e = ev.create("test_gc")
    with e:
        add("cmake")
        install()
        with capsys.disabled():
            assert "cmake" in find()
            output = gc("-y")
    assert "Restricting garbage collection" in output
    assert "There are no unused specs" in output


@pytest.mark.db
def test_gc_with_build_dependency_in_environment(
    config, mutable_database, mutable_mock_env_path, capsys
):
    s = spack.spec.Spec("simple-inheritance")
    s.concretize()
    s.package.do_install(fake=True, explicit=True)

    e = ev.create("test_gc")
    with e:
        add("simple-inheritance")
        install()
        with capsys.disabled():
            assert "simple-inheritance" in find()
            output = gc("-yb")
    assert "Restricting garbage collection" in output
    assert "There are no unused specs" in output

    with e:
        with capsys.disabled():
            assert "simple-inheritance" in find()
            output = gc("-y")
    assert "Restricting garbage collection" in output
    assert "Successfully uninstalled cmake" in output


@pytest.mark.db
def test_gc_except_any_environments(config, mutable_database, mutable_mock_env_path, capsys):
    s = spack.spec.Spec("simple-inheritance")
    s.concretize()
    s.package.do_install(fake=True, explicit=True)

    assert "zmpi" in find()

    e = ev.create("test_gc")
    with e:
        add("simple-inheritance")
        install()
        with capsys.disabled():
            assert "simple-inheritance" in find()

    output = gc("-yE")
    assert "Restricting garbage collection" not in output
    assert "Successfully uninstalled zmpi" in output
    assert "zmpi" not in find()


@pytest.mark.db
def test_gc_except_specific_environments(config, mutable_database, mutable_mock_env_path, capsys):
    s = spack.spec.Spec("simple-inheritance")
    s.concretize()
    s.package.do_install(fake=True, explicit=True)

    assert "zmpi" in find()

    e = ev.create("test_gc")
    with e:
        add("simple-inheritance")
        install()
        with capsys.disabled():
            assert "simple-inheritance" in find()

    output = gc("-ye", "test_gc")
    assert "Restricting garbage collection" not in output
    assert "Successfully uninstalled zmpi" in output
    assert "zmpi" not in find()
