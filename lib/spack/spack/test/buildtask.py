# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import pytest

import spack.error
import spack.installer as inst
import spack.repo
import spack.spec


def test_build_task_errors(install_mockery):
    kwargs = {
        "request": None,
        "compiler": "False",
        "start": "0",
        "attempts": "0",
        "status": "0",
        "installed": "mpileaks",
    }
    with pytest.raises(ValueError, match="must be a package"):
        inst.BuildTask(None, **kwargs)

    with pytest.raises(ValueError, match="must be a package"):
        inst.BuildTask("abc", **kwargs)

    spec = spack.spec.Spec("trivial-install-test-package")
    pkg_cls = spack.repo.PATH.get_pkg_class(spec.name)
    with pytest.raises(ValueError, match="must have a concrete spec"):
        inst.BuildTask(pkg_cls(spec), **kwargs)

    spec.concretize()
    assert spec.concrete
    with pytest.raises(ValueError, match="must be a BuildRequest"):
        inst.BuildTask(spec.package, **kwargs)

    kwargs["request"] = inst.BuildRequest(spec.package, {})
    with pytest.raises(ValueError, match="must be a BuildStatus"):
        inst.BuildTask(spec.package, **kwargs)

    kwargs["status"] = "queued"
    with pytest.raises(ValueError, match="must be a BuildStatus"):
        inst.BuildTask(spec.package, **kwargs)

    kwargs["status"] = inst.BuildStatus.REMOVED
    with pytest.raises(inst.InstallError, match="Cannot create a build task"):
        inst.BuildTask(spec.package, **kwargs)

    kwargs["status"] = inst.BuildStatus.INSTALLED
    with pytest.raises(ValueError, match="must be a bool"):
        inst.BuildTask(spec.package, **kwargs)

    kwargs["compiler"] = False
    with pytest.raises(ValueError, match="must be a float"):
        inst.BuildTask(spec.package, **kwargs)

    kwargs["start"] = 10.0
    with pytest.raises(ValueError, match="must be a set"):
        inst.BuildTask(spec.package, **kwargs)

    kwargs["installed"] = ["mpileaks"]
    with pytest.raises(ValueError, match="must be a set"):
        inst.BuildTask(spec.package, **kwargs)


def test_build_task_basics(install_mockery):
    spec = spack.spec.Spec("dependent-install")
    spec.concretize()
    assert spec.concrete

    # Ensure key properties match expectations
    request = inst.BuildRequest(spec.package, {})
    task = inst.BuildTask(spec.package, request=request, status=inst.BuildStatus.ADDED)
    assert not task.explicit
    assert task.priority == len(task.uninstalled_deps)
    assert task.key == (task.priority, task.sequence)

    # Ensure flagging installed works as expected
    assert len(task.uninstalled_deps) > 0
    assert task.dependencies == task.uninstalled_deps
    task.flag_installed(task.dependencies)
    assert len(task.uninstalled_deps) == 0
    assert task.priority == 0


def test_build_task_strings(install_mockery):
    """Tests of build_task repr and str for coverage purposes."""
    # Using a package with one dependency
    spec = spack.spec.Spec("dependent-install")
    spec.concretize()
    assert spec.concrete

    # Ensure key properties match expectations
    request = inst.BuildRequest(spec.package, {})
    task = inst.BuildTask(spec.package, request=request, status=inst.BuildStatus.ADDED)

    # Cover __repr__
    irep = task.__repr__()
    assert irep.startswith(task.__class__.__name__)
    assert "BuildStatus.ADDED" in irep
    assert "sequence=" in irep

    # Cover __str__
    istr = str(task)
    assert "status=queued" in istr  # == BuildStatus.ADDED
    assert "#dependencies=1" in istr
    assert "priority=" in istr
