# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import os
import os.path
import shutil

import pytest
import spack.binary_distribution
import spack.mirror
import spack.spec

install = spack.main.SpackCommand('install')


def test_build_tarball_overwrite(
        install_mockery, mock_fetch, monkeypatch, tmpdir):

    with tmpdir.as_cwd():
        spec = spack.spec.Spec('trivial-install-test-package').concretized()
        install(str(spec))

        # Runs fine the first time, throws the second time
        mirror = spack.mirror.MirrorCollection().lookup('.')
        spack.binary_distribution.build_tarball(spec, mirror, unsigned=True)
        with pytest.raises(spack.binary_distribution.NoOverwriteException):
            spack.binary_distribution.build_tarball(spec, mirror, unsigned=True)

        # Should work fine with force=True
        spack.binary_distribution.build_tarball(
            spec, mirror, force=True, unsigned=True)

        # Remove the tarball and try again.
        # This must *also* throw, because of the existing .spec.yaml file
        os.remove(os.path.join(
            spack.binary_distribution.build_cache_prefix('.'),
            spack.binary_distribution.tarball_directory_name(spec),
            spack.binary_distribution.tarball_name(spec, '.spack')))

        with pytest.raises(spack.binary_distribution.NoOverwriteException):
            spack.binary_distribution.build_tarball(spec, mirror, unsigned=True)


def test_build_tarball_split_mirror(install_mockery,
                                    mock_fetch, monkeypatch, tmpdir):

    with tmpdir.as_cwd():
        spec = spack.spec.Spec('trivial-install-test-package').concretized()
        install(str(spec))

        # Runs fine the first time, throws the second time
        mirror = spack.mirror.MirrorCollection().lookup('.')
        base_url = mirror.push_url
        mirror.push_url = base_url + '/push'
        mirror.fetch_url = base_url + '/fetch'
        spack.binary_distribution.build_tarball(spec, mirror, unsigned=True)
        # It exists in the push dir
        with pytest.raises(spack.binary_distribution.NoOverwriteException):
            spack.binary_distribution.build_tarball(spec, mirror, unsigned=True)
        # But now we force building anyway
        spack.binary_distribution.build_tarball(spec, mirror, force=True, unsigned=True)
        os.rename('push', 'fetch')
        # It now exists in the fetch dir, but not push
        with pytest.raises(spack.binary_distribution.NoOverwriteException):
            spack.binary_distribution.build_tarball(spec, mirror, unsigned=True)
        # But now we force the build anyway
        spack.binary_distribution.build_tarball(spec, mirror, force=True, unsigned=True)

        shutil.rmtree('push')
        # Delete all packages from the fetch directory
        # Remove the tarball and try again.
        # This must *also* throw, because of the existing .spec.yaml file
        os.remove(os.path.join(
            spack.binary_distribution.build_cache_prefix('fetch'),
            spack.binary_distribution.tarball_directory_name(spec),
            spack.binary_distribution.tarball_name(spec, '.spack')))
        with pytest.raises(spack.binary_distribution.NoOverwriteException):
            spack.binary_distribution.build_tarball(spec, mirror, unsigned=True)
        spack.binary_distribution.build_tarball(spec, mirror, force=True, unsigned=True)
        shutil.rmtree('push')
        os.rename('fetch', 'push')
        with pytest.raises(spack.binary_distribution.NoOverwriteException):
            spack.binary_distribution.build_tarball(spec, mirror, unsigned=True)
        spack.binary_distribution.build_tarball(spec, mirror, force=True, unsigned=True)
