# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Sp(CMakePackage):
    """The spectral transform library splib contains FORTRAN subprograms
    to be used for a variety of spectral transform functions. This is
    part of the NCEPLIBS project."""

    homepage = "https://noaa-emc.github.io/NCEPLIBS-sp"
    url      = "https://github.com/NOAA-EMC/NCEPLIBS-sp/archive/refs/tags/v2.3.3.tar.gz"

    maintainers = ['t-brown', 'kgerheiser', 'edwardhartnett', 'Hang-Lei-NOAA']

    version('2.3.3', sha256='c0d465209e599de3c0193e65671e290e9f422f659f1da928505489a3edeab99f')

    def setup_run_environment(self, env):
        for suffix in ('4', '8', 'd'):
            lib = find_libraries('libsp_' + suffix, root=self.prefix,
                                 shared=False, recursive=True)
            env.set('SP_LIB' + suffix, lib[0])
            env.set('SP_INC' + suffix, 'include_' + suffix)
