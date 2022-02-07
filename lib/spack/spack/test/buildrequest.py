# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import pytest

import spack.installer as inst
import spack.repo
import spack.spec


def test_build_request_errors(install_mockery):
    with pytest.raises(ValueError, match='must be a package'):
        inst.BuildRequest('abc', {})

    pkg = spack.repo.get('trivial-install-test-package')
    with pytest.raises(ValueError, match='must have a concrete spec'):
        inst.BuildRequest(pkg, {})


def test_build_request_basics(install_mockery):
    spec = spack.spec.Spec('dependent-install')
    spec.concretize()
    assert spec.concrete

    # Ensure key properties match expectations
    request = inst.BuildRequest(spec.package, {})
    assert not request.pkg.stop_before_phase
    assert not request.pkg.last_phase
    assert request.spec == spec.package.spec

    # Ensure key default install arguments are set
    assert 'install_package' in request.install_args
    assert 'install_deps' in request.install_args


def test_build_request_strings(install_mockery):
    """Tests of BuildRequest repr and str for coverage purposes."""
    # Using a package with one dependency
    spec = spack.spec.Spec('dependent-install')
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
