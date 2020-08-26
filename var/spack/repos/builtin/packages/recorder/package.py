# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

# ----------------------------------------------------------------------------
# If you submit this package back to Spack as a pull request,
# please first remove this boilerplate and all FIXME comments.
#
# This is a template package file for Spack.  We've put "FIXME"
# next to all the things you'll want to change. Once you've handled
# them, you can save this file and test your package like this:
#
#     spack install recorder
#
# You can edit this file again by typing:
#
#     spack edit recorder
#
# See the Spack documentation for more information on packaging.
# ----------------------------------------------------------------------------

from spack import *


class Recorder(AutotoolsPackage):
    """A multi-level library for understanding I/O activity in HPC applications."""

    # FIXME: Add a proper url for your package's homepage here.
    homepage = "https://github.com/uiuc-hpc/Recorder"
    url      = "https://github.com/uiuc-hpc/Recorder/archive/v2.1.4.tar.gz"

    # FIXME: Add a list of GitHub accounts to
    # notify when the package is updated.
    maintainers = ['wangvsa']

    version('2.1.4', sha256='f66756595a7f310929c247ae03fd08a18d9843f578fffa1e3072f557bf5a158e', preferred=True)

    depends_on('autoconf', type='build')
    depends_on('automake', type='build')
    depends_on('libtool',  type='build')
    depends_on('m4',       type='build')
    depends_on('mpi')
    depends_on('hdf5')

    variant('posix', default=True, description="Enable POSIX level tracing")
    variant('mpi', default=True, description="Enable MPI level tracing")
    variant('hdf5', default=True, description="Enable HDF5 level tracing")

    def autoreconf(self, spec, prefix):
        # FIXME: Modify the autoreconf method as necessary
        autoreconf('--install', '--verbose', '--force')

    def configure_args(self):
        args = []
        if "+posix" not in self.spec:
            args += ["--disable-posix"]
        if "+mpi" not in self.spec:
            args += ["--disable-mpi"]
        if "+hdf5" not in self.spec:
            args += ["--disable-hdf5"]

        return args
