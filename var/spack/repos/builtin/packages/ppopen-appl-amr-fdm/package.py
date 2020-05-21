# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *
import os


class PpopenApplAmrFdm(MakefilePackage):
    """
    ppOpen-APPL/AMR-FDM is an adaptive mesh refinement (AMR) framework
    for development of 3D parallel finite-difference method (FDM)
    applications.
    """

    homepage = "http://ppopenhpc.cc.u-tokyo.ac.jp/ppopenhpc/"
    url      = "file://{0}/ppohAMRFDM_0.3.0.tar.gz".format(os.getcwd())

    version('0.3.0', sha256='e82217e4c949dd079a56024d3d1c1761dc8efd5ad0d26a3af83564c3db7327bb')

    depends_on('mpi')

    parallel = False
    build_targets = ['default', 'advAMR3D']

    def edit(self, spec, prefix):
        fflags = [
            '-O3',
            '-I.',
            '-I{0}/include'.format(os.getcwd())
        ]
        makefile_in = FileFilter('Makefile.in')
        makefile_in.filter('^PREFIX +=.*', 'PREFIX = {0}'.format(prefix))
        makefile_in.filter(
            '^INCDIR +=.*',
            'INCDIR = {0}/include'.format(self.build_directory)
        )
        makefile_in.filter(
            '^LIBDIR +=.*',
            'LIBDIR = {0}/lib'.format(self.build_directory)
        )
        makefile_in.filter('^F90 +=.*', 'F90 = {0}'.format(spack_fc))
        makefile_in.filter(
            '^MPIF90 +=.*',
            'MPIF90 = {0}'.format(spec['mpi'].mpifc)
        )
        makefile_in.filter(
            '^sFFLAGS +=.*',
            'sFFLAGS = {0}'.format(' '.join(fflags))
        )
        fflags.append(self.compiler.openmp_flag)
        makefile_in.filter(
            '^pFFLAGS +=.*',
            'pFFLAGS = {0}'.format(' '.join(fflags))
        )

    def install(self, spec, prefix):
        install_tree('include', prefix.include)
        install_tree('lib', prefix.lib)
        install_tree('bin', prefix.bin)
        install_tree('doc', prefix.doc)
