# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import sys

import pytest

import spack.installer as inst
import spack.repo
import spack.spec

# Spack functionality tested here should work on Windows,
# however, tests are currently failing because support
# for Spack on Windows has not been extended to this
# module yet.
pytestmark = pytest.mark.skipif(sys.platform == "win32", reason="does not run on windows")


def test_build_request_errors(install_mockery):
    with pytest.raises(ValueError, match="must be a package"):
        inst.BuildRequest("abc", {})

    spec = spack.spec.Spec("trivial-install-test-package")
    pkg_cls = spack.repo.path.get_pkg_class(spec.name)
    with pytest.raises(ValueError, match="must have a concrete spec"):
        inst.BuildRequest(pkg_cls(spec), {})


def test_build_request_basics(install_mockery):
    spec = spack.spec.Spec("dependent-install")
    spec.concretize()
    assert spec.concrete

    # Ensure key properties match expectations
    request = inst.BuildRequest(spec.package, {})
    assert not request.pkg.stop_before_phase
    assert not request.pkg.last_phase
    assert request.spec == spec.package.spec

    # Ensure key default install arguments are set
    assert "install_package" in request.install_args
    assert "install_deps" in request.install_args


def test_build_request_strings(install_mockery):
    """Tests of BuildRequest repr and str for coverage purposes."""
    # Using a package with one dependency
    spec = spack.spec.Spec("dependent-install")
    spec.concretize()
    assert spec.concrete

    # Ensure key properties match expectations
    request = inst.BuildRequest(spec.package, {})

    # Cover __repr__
    irep = request.__repr__()
    assert irep.startswith(request.__class__.__name__)

    # Cover __str__
    istr = str(request)
    assert "package=dependent-install" in istr
    assert "install_args=" in istr


@pytest.mark.parametrize(
    "package_cache_only,dependencies_cache_only,package_deptypes,dependencies_deptypes",
    [
        (False, False, ["build", "link", "run"], ["build", "link", "run"]),
        (True, False, ["link", "run"], ["build", "link", "run"]),
        (False, True, ["build", "link", "run"], ["link", "run"]),
        (True, True, ["link", "run"], ["link", "run"]),
    ],
)
def test_build_request_deptypes(
    install_mockery,
    package_cache_only,
    dependencies_cache_only,
    package_deptypes,
    dependencies_deptypes,
):
    s = spack.spec.Spec("dependent-install").concretized()

    build_request = inst.BuildRequest(
        s.package,
        {
            "package_cache_only": package_cache_only,
            "dependencies_cache_only": dependencies_cache_only,
        },
    )

    actual_package_deptypes = build_request.get_deptypes(s.package)
    actual_dependency_deptypes = build_request.get_deptypes(s["dependency-install"].package)

    assert sorted(actual_package_deptypes) == package_deptypes
    assert sorted(actual_dependency_deptypes) == dependencies_deptypes
