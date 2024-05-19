# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import os
import os.path

import pytest

import spack.binary_distribution as bd
import spack.main
import spack.spec
import spack.util.url

install = spack.main.SpackCommand("install")

pytestmark = pytest.mark.not_on_windows("does not run on windows")


def test_build_tarball_overwrite(install_mockery, mock_fetch, monkeypatch, tmpdir):
    with tmpdir.as_cwd():
        spec = spack.spec.Spec("trivial-install-test-package").concretized()
        install(str(spec))

        # Runs fine the first time, throws the second time
        out_url = spack.util.url.path_to_file_url(str(tmpdir))
        bd.push_or_raise(spec, out_url, bd.PushOptions(unsigned=True))
        with pytest.raises(bd.NoOverwriteException):
            bd.push_or_raise(spec, out_url, bd.PushOptions(unsigned=True))

        # Should work fine with force=True
        bd.push_or_raise(spec, out_url, bd.PushOptions(force=True, unsigned=True))

        # Remove the tarball and try again.
        # This must *also* throw, because of the existing .spec.json file
        os.remove(
            os.path.join(
                bd.build_cache_prefix("."),
                bd.tarball_directory_name(spec),
                bd.tarball_name(spec, ".spack"),
            )
        )

        with pytest.raises(bd.NoOverwriteException):
            bd.push_or_raise(spec, out_url, bd.PushOptions(unsigned=True))
