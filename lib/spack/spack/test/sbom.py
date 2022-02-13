# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import os

import pytest

import spack.sbom
import spack.spec
import spack.util.spack_json as sjson
from spack.main import SpackCommand

sbom_cmd = SpackCommand('sbom')


@pytest.fixture(autouse=True)
def restore_generation_state():
    """
    Restore original state before and after tests
    """
    spack.sbom.generate_sbom = False
    yield
    spack.sbom.generate_sbom = False


def test_sbom_install_flag(install_mockery, mock_fetch):
    """
    Mock installing package with sbom
    """
    # Install with --sbom generates it
    spec = spack.spec.Spec("dttop")
    spec.concretize()
    spec.package.do_install(force=True)
    spack.sbom.create_sbom(spec)
    assert os.path.exists(spec.sbom)


def test_sbom_install_flag_absent(install_mockery, mock_fetch):
    # Install without --sbom does not generates it
    spec = spack.spec.Spec("dttop")
    spec.concretize()
    spec.package.do_install(force=True)
    assert not os.path.exists(spec.sbom)


def test_sbom_create(install_mockery, mock_fetch):
    """
    Sbom show should output json
    """
    spec = spack.spec.Spec("dttop")
    spec.concretize()
    spec.package.do_install(force=True)
    assert not os.path.exists(spec.sbom)
    out = sbom_cmd('create', 'dttop')
    assert "sbom generated successfully" in out
    assert os.path.exists(spec.sbom)

    # We can't create if not installed
    spec.package.do_uninstall(force=True)
    out = sbom_cmd('create', 'dttop', fail_on_error=False)
    assert "not installed" in out


def test_sbom_show_path(install_mockery, mock_fetch):
    """
    Sbom show should output json
    """
    spec = spack.spec.Spec("dttop")
    spec.concretize()
    spec.package.do_install(force=True)
    spack.sbom.create_sbom(spec)
    out = sbom_cmd('show', 'dttop')
    sjson.load(out)
