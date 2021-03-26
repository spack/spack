# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.main import SpackCommand


cd = SpackCommand('cd')


def test_cd(capsys):
    """Sanity check the cd command to make sure it works."""

    out = cd(out=capsys)

    assert "To set up shell support" in out
