# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import spack.concretize


def test_default_variant(config, mock_packages):
    spec = spack.concretize.concretize_one("optional-dep-test-3")
    assert "pkg-a" in spec

    spec = spack.concretize.concretize_one("optional-dep-test-3~var")
    assert "pkg-a" in spec

    spec = spack.concretize.concretize_one("optional-dep-test-3+var")
    assert "pkg-b" in spec
