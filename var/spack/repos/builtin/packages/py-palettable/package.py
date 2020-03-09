# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyPalettable(PythonPackage):
    """Color palettes for Python."""

    homepage = "https://jiffyclub.github.io/palettable/"
    url      = "https://pypi.io/packages/source/p/palettable/palettable-3.0.0.tar.gz"

    version('3.0.0', sha256='eed9eb0399386ff42f90ca61d4fa38a1819a93d5adfc2d546e3e2869d9972c31')

    depends_on('py-setuptools', type='build')
