# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
""" Test ABI compatibility helpers"""

import pytest

from spack.abi import ABI
from spack.spec import Spec


@pytest.mark.parametrize(
    "target,constraint,expected",
    [
        ("foo", "bar", True),
        ("platform=linux", "foo", True),
        ("foo", "arch=linux-fedora31-x86_64", True),
        ("arch=linux-fedora31-skylake", "arch=linux-fedora31-skylake", True),
        ("arch=linux-fedora31-skylake", "arch=linux-fedora31-x86_64", False),
        ("platform=linux os=fedora31", "arch=linux-fedora31-x86_64", True),
        ("platform=linux", "arch=linux-fedora31-x86_64", True),
        ("platform=linux os=fedora31", "platform=linux", True),
        ("platform=darwin", "arch=linux-fedora31-x86_64", False),
        ("os=fedora31", "platform=linux", True),
    ],
)
def test_architecture_compatibility(target, constraint, expected):
    assert ABI().architecture_compatible(Spec(target), Spec(constraint)) == expected


@pytest.mark.parametrize(
    "target,constraint,loose,expected",
    [
        ("foo", "bar", False, True),
        ("%gcc", "foo", False, True),
        ("foo", "%gcc", False, True),
        ("%gcc", "%gcc", False, True),
        ("%gcc", "%intel", False, False),
        ("%gcc", "%clang", False, False),
        ("%gcc@9.1", "%gcc@9.2", False, False),  # TODO should be true ?
        ("%gcc@9.2.1", "%gcc@9.2.2", False, False),  # TODO should be true ?
        ("%gcc@4.9", "%gcc@9.2", False, False),
        ("%clang@5", "%clang@6", False, False),
        ("%gcc@9.1", "%gcc@9.2", True, True),
        ("%gcc@9.2.1", "%gcc@9.2.2", True, True),
        ("%gcc@4.9", "%gcc@9.2", True, True),
        ("%clang@5", "%clang@6", True, True),
    ],
)
def test_compiler_compatibility(target, constraint, loose, expected):
    assert ABI().compiler_compatible(Spec(target), Spec(constraint), loose=loose) == expected


@pytest.mark.parametrize(
    "target,constraint,loose,expected",
    [
        ("foo", "bar", False, True),
        ("%gcc", "platform=linux", False, True),
        ("%gcc@9.2.1", "%gcc@8.3.1 platform=linux", False, False),
        ("%gcc@9.2.1", "%gcc@8.3.1 platform=linux", True, True),
        ("%gcc@9.2.1 arch=linux-fedora31-skylake", "%gcc@9.2.1 platform=linux", False, True),
    ],
)
def test_compatibility(target, constraint, loose, expected):
    assert ABI().compatible(Spec(target), Spec(constraint), loose=loose) == expected
