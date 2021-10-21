# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import sys

import pytest

import spack.environment as ev
import spack.main
import spack.spec

gc = spack.main.SpackCommand('gc')


@pytest.mark.skipif(sys.platform == "win32", reason="Test unsupported on Windows")
@pytest.mark.db
def test_no_packages_to_remove(config, mutable_database, capsys):
    with capsys.disabled():
        output = gc('-y')
    assert 'There are no unused specs.' in output


@pytest.mark.skipif(sys.platform == "win32", reason="Test unsupported on Windows")
@pytest.mark.db
def test_packages_are_removed(config, mutable_database, capsys):
    s = spack.spec.Spec('simple-inheritance')
    s.concretize()
    s.package.do_install(fake=True, explicit=True)
    with capsys.disabled():
        output = gc('-y')
    assert 'Successfully uninstalled cmake' in output


@pytest.mark.skipif(sys.platform == "win32", reason="Test unsupported on Windows")
@pytest.mark.db
def test_gc_with_environment(
        config, mutable_database, mutable_mock_env_path, capsys
):
    s = spack.spec.Spec('simple-inheritance')
    s.concretize()
    s.package.do_install(fake=True, explicit=True)

    e = ev.create('test_gc')
    e.add('cmake')
    with e:
        with capsys.disabled():
            output = gc('-y')
    assert 'Restricting the garbage collection' in output
    assert 'There are no unused specs' in output
