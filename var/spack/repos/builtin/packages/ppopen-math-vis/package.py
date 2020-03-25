# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack import *
import os


class PpopenMathVis(MakefilePackage):
    """
    ppOpen-MATH/VIS is a set of libraries for parallel visualization.

    Capabilities of ppOpen-MATH/VIS (ver.0.2.0) are as follows:

    Using background voxels with adaptive mesh refinement (AMR).
    Single UCD file.
    Flat MPI parallel programming models.
    (OpenMP/MPI hybrid will be supported in the future).
    Can be called from programs written in both of Fortran 90 and C.
    Only FDM-type structured meshes are supported.
    """

    homepage = "http://ppopenhpc.cc.u-tokyo.ac.jp/ppopenhpc/"
    url = "file://{0}/ppohVIS_0.2.0.tar.gz".format(os.getcwd())

    version('0.2.0', sha256='f816885cb9fab4802f9df55c1f1e7f8505867dc8862562bce26d193d6a0dc29d')

    depends_on('mpi')

    def edit(self, spec, prefix):
        makefile_in = FileFilter('Makefile.in')
        makefile_in.filter('mpifccpx', spec['mpi'].mpicc)
        makefile_in.filter('mpiFCCpx', spec['mpi'].mpicxx)
        makefile_in.filter('mpifrtpx', spec['mpi'].mpifc)
        makefile_in.filter('-Kfast', '-O3')
        makefile_in.filter(r'~/ppOpen-HPC/.*', prefix)

    @run_after('install')
    def sample_install(self):
        mkdir(join_path(self.prefix, 'examples'))
        copy_tree('examples', join_path(self.prefix, 'examples'))
        mkdir(join_path(self.prefix, 'doc'))
        copy_tree('doc', join_path(self.prefix, 'doc'))
