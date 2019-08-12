# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyPalettable(PythonPackage):
    """Color palettes for Python."""

    homepage = "https://jiffyclub.github.io/palettable/"
    url      = "https://pypi.io/packages/source/p/palettable/palettable-3.0.0.tar.gz"

    version('3.0.0', '6e430319fe01386c81dbbc62534e3cc4')

    depends_on('py-setuptools', type='build')
