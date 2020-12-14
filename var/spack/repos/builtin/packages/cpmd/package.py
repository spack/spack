# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *
import os
import shutil


class Cpmd(MakefilePackage):
    """The CPMD code is a parallelized plane wave / pseudopotential
    implementation of Density Functional Theory, particularly
    designed for ab-initio molecular dynamics."""

    homepage = "https://www.cpmd.org/wordpress/"
    url = "file://{0}/cpmd-v4.3.tar.gz".format(os.getcwd())

    version(
        '4.3', sha256='4f31ddf045f1ae5d6f25559d85ddbdab4d7a6200362849df833632976d095df4')

    # Patch to ver4624
    patch('cpmd_4624.patch', when='@4.3')

    #variant('mpi', description='Build MPI executables',
            #default=True)

    depends_on('lapack')
    #depends_on('mpi', when='+mpi')

    def edit(self, spec, prefix):
        # patch configure file
        cp = join_path('configure', 'LINUX-GFORTRAN')
        # Compilers
        filter_file(
            'FC=.+',
            'FC=\'{0}\''.format(spack_fc),
            cp
        )
        filter_file(
            'CC=.+',
            'CC=\'{0}\''.format(spack_cc),
            cp
        )
        filter_file(
            'LD=.+',
            'LD=\'{0}\''.format(spack_fc),
            cp
        )
        # lapack
        filter_file(
            'LIBS=.+',
            'LIBS=\'{0}\''.format(spec['lapack'].libs.ld_flags),
            cp
        )
        filter_file(
            '\'-static \'',
            '',
            cp
        )
        # create Makefile
        bash = which('bash')
        bash('./configure.sh', 'LINUX-GFORTRAN')

    def install(self, spec, prefix):
        # just install bin/cpmd.x
        install_tree('bin', prefix.bin)
