# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


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
    url      = "https://gitlab.kitware.com/api/v4/projects/vtk%2Fvtk-m/repository/archive.tar.gz?sha=v1.1.0"
    git      = "https://gitlab.kitware.com/vtk/vtk-m.git"

    version('master', branch='master')
    version('1.1.0', "6aab1c0885f6ffaaffcf07930873d0df")

    variant("cuda", default=False, description="build cuda support")
    variant("tbb", default=True, description="build TBB support")

    depends_on("cmake")
    depends_on("tbb", when="+tbb")
    depends_on("cuda", when="+cuda")

    def install(self, spec, prefix):
        with working_dir('spack-build', create=True):
            cmake_args = ["../",
                          "-DVTKm_ENABLE_TESTING=OFF",
                          "-DVTKm_BUILD_RENDERING=ON",
                          "-DVTKm_USE_64BIT_IDS=OFF",
                          "-DVTKm_USE_DOUBLE_PRECISION=ON"]
            # tbb support
            if "+tbb" in spec:
                # vtk-m detectes tbb via TBB_ROOT env var
                os.environ["TBB_ROOT"] = spec["tbb"].prefix
                cmake_args.append("-DVTKm_ENABLE_TBB=ON")

            # cuda support
            if "+cuda" in spec:
                cmake_args.append("-DVTKm_ENABLE_CUDA=ON")
                # this fix is necessary if compiling platform has cuda, but
                # no devices (this common for front end nodes on hpc clusters)
                # we choose kepler as a lowest common denominator
                cmake_args.append("-DVTKm_CUDA_Architecture=kepler")

            # use release, instead of release with debug symbols b/c vtkm libs
            # can overwhelm compilers with too many symbols
            for arg in std_cmake_args:
                if arg.count("CMAKE_BUILD_TYPE") == 0:
                    cmake_args.extend(std_cmake_args)
            cmake_args.append("-DCMAKE_BUILD_TYPE=Release")
            cmake(*cmake_args)
            make()
            make("install")
