# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyElephant(PythonPackage):
    """Elephant is a package for analysis of electrophysiology data in Python
    """

    homepage = "http://neuralensemble.org/elephant"
    url      = "https://pypi.io/packages/source/e/elephant/elephant-0.3.0.tar.gz"

    version('0.4.1', '0e6214c96cae6ce777e4b3cf29bbdaa9')
    version('0.3.0', '84e69e6628fd617af469780c30d2da6c')

    variant('doc', default=False, description='Build the documentation')
    variant('pandas', default=True, description='Build with pandas')

    depends_on('py-setuptools',         type='build')
    depends_on('py-neo@0.3.4:',         type=('build', 'run'))  # > 0.3.3 ?
    depends_on('py-numpy@1.8.2:',       type=('build', 'run'))
    depends_on('py-quantities@0.10.1:', type=('build', 'run'))
    depends_on('py-scipy@0.14.0:',      type=('build', 'run'))
    depends_on('py-pandas@0.14.1:',     type=('build', 'run'), when='+pandas')
    depends_on('py-numpydoc@0.5:',      type=('build', 'run'), when='+docs')
    depends_on('py-sphinx@1.2.2:',      type=('build', 'run'), when='+docs')
    depends_on('py-nose@1.3.3:',        type='test')
