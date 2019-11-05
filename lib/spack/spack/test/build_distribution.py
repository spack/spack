# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import pytest

import os
import os.path

import spack.spec
import spack.binary_distribution

install = spack.main.SpackCommand('install')


def test_build_tarball_overwrite(install_mockery, mock_fetch, monkeypatch):
    spec = spack.spec.Spec('trivial-install-test-package').concretized()
    install(str(spec))

    outdir = '.'

    # Might possibly throw the first time
    try:
        spack.binary_distribution.build_tarball(spec, outdir, unsigned=True)
    except spack.binary_distribution.NoOverwriteException:
        pass

    # *Must* throw the second time
    with pytest.raises(spack.binary_distribution.NoOverwriteException):
        spack.binary_distribution.build_tarball(spec, outdir, unsigned=True)

    # Should work fine with force=True
    spack.binary_distribution.build_tarball(
        spec, outdir, force=True, unsigned=True)

    # Remove the tarball and try again.
    # This must *also* throw, because of the existing .spec.yaml file
    os.remove(os.path.join(
        spack.binary_distribution.build_cache_prefix(outdir),
        spack.binary_distribution.tarball_directory_name(spec),
        spack.binary_distribution.tarball_name(spec, '.spack')))

    with pytest.raises(spack.binary_distribution.NoOverwriteException):
        spack.binary_distribution.build_tarball(spec, outdir, unsigned=True)
