# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyBiomFormat(PythonPackage):
    """The BIOM file format (canonically pronounced biome) is designed to be
       a general-use format for representing biological sample by observation
       contingency tables."""

    homepage = "http://biom-format.org/"
    url      = "https://github.com/biocore/biom-format/archive/2.1.10.tar.gz"

    version('2.1.10', sha256='b63ce742dbe7d2353a48e004096645e9e2e4f7d53802e2c5d044f108b873a204')
    version('2.1.9',  sha256='fce4ef925ef1a1594b16680f11c76e0ba245c0fda4286f3632a1bd4be36434c7')
    version('2.1.8',  sha256='91cae2e11702c763eeb8a4e1db3cf120e7cdaae8cc38aaae7163be74e6cff77a')
    version('2.1.7',  sha256='88b3ef16fd7d16f4e125f1e0d356aaad4c7c281ea3fb746c0f8dc26f3a5b6d4d')
    version('2.1.6', sha256='8eefc275a85cc937f6d6f408d91b7b45eae854cd5d1cbda411a3af51f5b49b0d')

    variant('h5py', default=True, description='For use with BIOM 2.0+ files')
    variant('pyqi', default=False, description='For use when using biom-format 2.1.6')

    depends_on('py-setuptools', type=('build', 'run'))
    depends_on('py-cython', type='build')
    depends_on('py-h5py', type=('build', 'run'), when='+h5py')
    depends_on('py-click', type=('build', 'run'))
    depends_on('py-numpy@1.3.0:', type=('build', 'run'))
    depends_on('py-future@0.16.0:', type=('build', 'run'))
    depends_on('py-scipy@0.13.0:', type=('build', 'run'))
    depends_on('py-pandas@0.19.2:', type=('build', 'run'))
    depends_on('py-six@1.10.0:', type=('build', 'run'))
    depends_on('py-pyqi', type=('build', 'run'), when='+pyqi')
