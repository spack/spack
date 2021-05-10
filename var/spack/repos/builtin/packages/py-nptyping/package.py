# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyNptyping(PythonPackage):
    """Type hints for numpy"""
    homepage = "https://github.com/ramonhagenaars/nptyping"
    url      = "https://github.com/ramonhagenaars/nptyping/archive/v1.4.1.tar.gz"

    version('1.4.1', sha256='bbcedb967f8be1302dffdd999eb531b99712c6914078294b4411758d5899b3b6')
    version('1.0.1', sha256='a00e672bfdaddc99aa6b25dd1ae89d7d58d2b76e8ad099bd69577bac2598589f')

    depends_on('py-setuptools', type='build')
    depends_on('py-typish@1.7.0:', type=('build', 'run'))
    depends_on('py-numpy', type=('build', 'run'))
