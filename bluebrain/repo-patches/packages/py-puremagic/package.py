# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyPuremagic(PythonPackage):
    """puremagic is a pure python module that will identify a file based
    off it's magic numbers.
    """
    homepage = "https://github.com/cdgriffith/puremagic"
    url = "https://pypi.io/packages/source/p/puremagic/puremagic-1.10.tar.gz"

    version('1.10', sha256='6ffea02b80ceec1381f9df513e0120b701a74b6efad92311ea80281c7081b108')

    depends_on('py-setuptools', type='build')
    depends_on('py-argparse', type=('build', 'run'))
