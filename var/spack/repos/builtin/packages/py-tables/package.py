# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyTables(PythonPackage):
    """
PyTables is a package for managing hierarchical datasets and designed to
efficiently cope with extremely large amounts of data.

It is built on top of the HDF5 library and the NumPy package. It features an
object-oriented interface that, combined with C extensions for the
performance-critical parts of the code (generated using Cython), makes it a
fast, yet extremely easy to use tool for interactively save and retrieve very
large amounts of data. One important feature of PyTables is that it optimizes
memory and disk resources so that they take much less space (between a factor 3
to 5, and more if the data is compressible) than other solutions, like for
example, relational or object oriented databases.
    """

    homepage = "http://www.pytables.org/"
    url      = "https://github.com/PyTables/PyTables/archive/v3.5.1.tar.gz"

    version('3.5.1',
      sha256='fda2e5071ce064ae1e808623e4c6166e6ab5f0f6152043991c5151d4e2622f2e')

    depends_on('hdf5@1.8.15:+hl', type=('build', 'link', 'run'))
    depends_on('py-numpy@1.9.3:', type=('build', 'run'))
    depends_on('py-numexpr@2.6.2:', type=('build', 'run'))
    depends_on('py-cython@0.21:', type=('build', 'run'))
    depends_on('c-blosc@1.4.1:', type=('build', 'run'))

    def setup_environment(self, spack_env, run_env):
        spack_env.set('HDF5_DIR', self.spec['hdf5'].prefix)
