# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Kallisto(CMakePackage):
    """kallisto is a program for quantifying abundances of transcripts from
       RNA-Seq data."""

    homepage = "http://pachterlab.github.io/kallisto"
    url      = "https://github.com/pachterlab/kallisto/archive/v0.43.1.tar.gz"

    version('0.46.2', sha256='c447ca8ddc40fcbd7d877d7c868bc8b72807aa8823a8a8d659e19bdd515baaf2')
    version('0.43.1', sha256='7baef1b3b67bcf81dc7c604db2ef30f5520b48d532bf28ec26331cb60ce69400')

    depends_on('zlib')
    depends_on('hdf5')
    depends_on('mpich')

    depends_on('autoconf', type='build')
    depends_on('automake', type='build')
    depends_on('libtool',  type='build')
    depends_on('m4',       type='build')

    # Including '-DCMAKE_VERBOSE_MAKEFILE:BOOL=ON' in the cmake args
    # causes bits of cmake's output to end up in the autoconf-generated
    # configure script.
    # See https://github.com/spack/spack/issues/15274 and
    # https://github.com/pachterlab/kallisto/issues/253
    @property
    def std_cmake_args(self):
        """Call the original std_cmake_args and then filter the verbose
        setting.
        """
        a = super(Kallisto, self).std_cmake_args
        args = [i for i in a if i != '-DCMAKE_VERBOSE_MAKEFILE:BOOL=ON']

        return args
