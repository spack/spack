# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RRhdf5filters(RPackage):
    """HDF5 Compression Filters.

    Provides a collection of compression filters for use with HDF5 datasets."""

    bioc = "rhdf5filters"

    version('1.6.0', commit='5f7f3a5b7dabd6e7d0c50cda70290e2472ff4f53')
    version('1.2.0', commit='25af0180f926b4b3ea11b30ec9277d26ad3d56b3')

    depends_on('r-rhdf5lib', type=('build', 'run'))
    depends_on('gmake', type='build')

    def configure_args(self):
        args = []
        if self.spec.target.family == 'aarch64':
            args.append("ax_cv_gcc_check_x86_cpu_init=yes")
            args.append("ax_cv_gcc_x86_cpu_supports_sse2=no")
        return args
