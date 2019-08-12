# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyBiomFormat(PythonPackage):
    """The BIOM file format (canonically pronounced biome) is designed to be
       a general-use format for representing biological sample by observation
       contingency tables."""

    homepage = "https://pypi.python.org/pypi/biom-format/2.1.6"
    url      = "https://pypi.io/packages/source/b/biom-format/biom-format-2.1.6.tar.gz"

    version('2.1.6', '1dd4925b74c56e8ee864d5e1973068de')

    variant('h5py', default=True, description='For use with BIOM 2.0+ files')

    depends_on('py-setuptools', type=('build', 'run'))
    depends_on('py-cython', type='build')
    depends_on('py-h5py', type=('build', 'run'), when='+h5py')
    depends_on('py-click', type=('build', 'run'))
    depends_on('py-numpy@1.3.0:', type=('build', 'run'))
    depends_on('py-future@0.16.0:', type=('build', 'run'))
    depends_on('py-scipy@0.13.0:', type=('build', 'run'))
    depends_on('py-pandas@0.19.2:', type=('build', 'run'))
    depends_on('py-six@1.10.0:', type=('build', 'run'))
    depends_on('py-pyqi', type=('build', 'run'))
