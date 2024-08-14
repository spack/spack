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

pytestmark = pytest.mark.not_on_windows("does not run on windows")


def test_build_tarball_overwrite(install_mockery, mock_fetch, monkeypatch, tmp_path):
    spec = spack.spec.Spec("trivial-install-test-package").concretized()
    spec.package.do_install(fake=True)

    specs = [spec]

    # Runs fine the first time, second time it's a no-op
    out_url = spack.util.url.path_to_file_url(str(tmp_path))
    skipped = bd.push_or_raise(specs, out_url, signing_key=None)
    assert not skipped

    skipped = bd.push_or_raise(specs, out_url, signing_key=None)
    assert skipped == specs

    # Should work fine with force=True
    skipped = bd.push_or_raise(specs, out_url, signing_key=None, force=True)
    assert not skipped

    # Remove the tarball, which should cause push to push.
    os.remove(
        tmp_path
        / bd.BUILD_CACHE_RELATIVE_PATH
        / bd.tarball_directory_name(spec)
        / bd.tarball_name(spec, ".spack")
    )

    skipped = bd.push_or_raise(specs, out_url, signing_key=None)
    assert not skipped
