##############################################################################
# Copyright (c) 2013-2018, Lawrence Livermore National Security, LLC.
# Produced at the Lawrence Livermore National Laboratory.
#
# This file is part of Spack.
# Created by Todd Gamblin, tgamblin@llnl.gov, All rights reserved.
# LLNL-CODE-647188
#
# For details, see https://github.com/spack/spack
# Please also see the NOTICE and LICENSE files for our notice and the LGPL.
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License (as
# published by the Free Software Foundation) version 2.1, February 1999.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the IMPLIED WARRANTY OF
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the terms and
# conditions of the GNU Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public
# License along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA 02111-1307 USA
##############################################################################

from spack import *
import os


class Vtkm(Package):
    """VTK-m is a toolkit of scientific visualization algorithms for emerging
    processor architectures. VTK-m supports the fine-grained concurrency for
    data analysis and visualization algorithms required to drive extreme scale
    computing by providing abstract models for data and execution that can be
    applied to a variety of algorithms across many different processor
    architectures."""

    homepage = "https://m.vtk.org/"
    url      = "https://gitlab.kitware.com/vtk/vtk-m/repository/v1.2.0/archive.tar.gz"

    version('1.2.0', "f77604c5a1c1747f2fb9b9bd96476875")

    version('1.1.0', "6aab1c0885f6ffaaffcf07930873d0df")

    version('master',
            git='https://gitlab.kitware.com/vtk/vtk-m.git',
            branch='master')

    variant("shared", default=True, description="Build vtk-m as shared libs")
    
    variant("cuda", default=False, description="build cuda support")
    variant("tbb", default=True, description="build TBB support")
    variant("openmp", default=False, description="build OpenMP support")

    depends_on("cmake@3.8.2:3.9.999")
    depends_on("tbb", when="+tbb")
    depends_on("intel-tbb~shared", when="+tbb~shared")
    depends_on("cuda", when="+cuda")

    def install(self, spec, prefix):
        with working_dir('spack-build', create=True):
            cmake_args = ["../",
                          "-DVTKm_ENABLE_TESTING=OFF",
                          "-DVTKm_BUILD_RENDERING=ON",
                          "-DVTKm_USE_64BIT_IDS=OFF",
                          "-DVTKm_USE_DOUBLE_PRECISION=ON"]
            # shared vs static libs
            if "+shared" in spec:
                cmake_args.append('-DBUILD_SHARED_LIBS=ON')
            else:
                cmake_args.append('-DBUILD_SHARED_LIBS=OFF')

            # tbb support
            if "+tbb" in spec:
                # vtk-m detectes tbb via TBB_ROOT env var
                os.environ["TBB_ROOT"] = spec["intel-tbb"].prefix
                cmake_args.append("-DVTKm_ENABLE_TBB=ON")

            # cuda support
            if "+cuda" in spec:
                cmake_args.append("-DVTKm_ENABLE_CUDA=ON")
                # this fix is necessary if compiling platform has cuda, but
                # no devices (this common for front end nodes on hpc clusters)
                # we choose kepler as a lowest common denominator
                cmake_args.append("-DVTKm_CUDA_Architecture=kepler")

            # openmp support
            if "+openmp" in spec:
                cmake_args.append("-DVTKm_ENABLE_OPENMP=ON")

            # use release, instead of release with debug symbols b/c vtkm libs
            # can overwhelm compilers with too many symbols
            for arg in std_cmake_args:
                if arg.count("CMAKE_BUILD_TYPE") == 0:
                    cmake_args.extend(std_cmake_args)
            cmake_args.append("-DCMAKE_BUILD_TYPE=Release")
            cmake(*cmake_args)
            make()
            make("install")
