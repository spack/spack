# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import spack
from spack.main import SpackCommand

python = SpackCommand('python')


def test_python():
    out = python('-c', 'import spack; print(spack.spack_version)')
    assert out.strip() == spack.spack_version
