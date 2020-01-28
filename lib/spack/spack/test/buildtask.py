# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import pytest

import spack.installer as inst
import spack.repo
import spack.spec


def test_build_task_errors(install_mockery):
    with pytest.raises(ValueError, match='must be a package'):
        inst.BuildTask('abc', False, 0, 0, 0, [])

    pkg = spack.repo.get('trivial-install-test-package')
    with pytest.raises(ValueError, match='must have a concrete spec'):
        inst.BuildTask(pkg, False, 0, 0, 0, [])

    spec = spack.spec.Spec('trivial-install-test-package')
    spec.concretize()
    assert spec.concrete
    with pytest.raises(inst.InstallError, match='Cannot create a build task'):
        inst.BuildTask(spec.package, False, 0, 0, inst.STATUS_REMOVED, [])


def test_build_task_basics(install_mockery):
    spec = spack.spec.Spec('dependent-install')
    spec.concretize()
    assert spec.concrete

    # Ensure key properties match expectations
    task = inst.BuildTask(spec.package, False, 0, 0, inst.STATUS_ADDED, [])
    assert task.priority == len(task.uninstalled_deps)
    assert task.key == (task.priority, task.sequence)

    # Ensure flagging installed works as expected
    assert len(task.uninstalled_deps) > 0
    assert task.dependencies == task.uninstalled_deps
    task.flag_installed(task.dependencies)
    assert len(task.uninstalled_deps) == 0
    assert task.priority == 0
