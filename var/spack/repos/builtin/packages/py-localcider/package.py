# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyLocalcider(PythonPackage):
    """Tools for calculating sequence properties of disordered proteins"""

    homepage = "http://pappulab.github.io/localCIDER"
    url      = "https://pypi.io/packages/source/l/localcider/localcider-0.1.14.tar.gz"

    version('0.1.14', 'cd3c992595c5cb280374de3750663cfa')

    depends_on('py-setuptools', type='build')
    depends_on('py-numpy',        type=('build', 'run'))
    depends_on('py-matplotlib',   type=('build', 'run'))
    depends_on('py-scipy',        type=('build', 'run'))
