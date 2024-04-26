# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
import pytest

from spack.util import libc


@pytest.mark.parametrize(
    "startfile_prefix,expected",
    [
        # Ubuntu
        ("/usr/lib/x86_64-linux-gnu", "/usr/include/x86_64-linux-gnu"),
        ("/usr/lib/x86_64-linux-musl", "/usr/include/x86_64-linux-musl"),
        ("/usr/lib/aarch64-linux-gnu", "/usr/include/aarch64-linux-gnu"),
        ("/usr/lib/aarch64-linux-musl", "/usr/include/aarch64-linux-musl"),
        # rhel-like
        ("/usr/lib64", "/usr/include"),
        ("/usr/lib", "/usr/include"),
    ],
)
@pytest.mark.not_on_windows("The unit test deals with unix-like paths")
def test_header_dir_computation(startfile_prefix, expected):
    """Tests that we compute the correct header directory from the prefix of the libc startfiles"""
    assert libc.libc_include_dir_from_startfile_prefix(startfile_prefix) == expected
