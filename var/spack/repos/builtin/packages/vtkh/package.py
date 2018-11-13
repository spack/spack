# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack import *
import os


class Vtkh(Package):
    """VTK-h is a toolkit of scientific visualization algorithms for emerging
    processor architectures. VTK-h brings together several projects like VTK-m
    and DIY2 to provide a toolkit with hybrid parallel capabilities."""

    homepage = "https://github.com/Alpine-DAV/vtk-h"
    git      = "https://github.com/Alpine-DAV/vtk-h.git"

    version('master', branch='master', submodules=True)

    maintainers = ['cyrush']

    variant("mpi", default=True, description="build mpi support")
    variant("tbb", default=True, description="build tbb support")
    variant("cuda", default=False, description="build cuda support")

    depends_on("cmake")

    depends_on("mpi", when="+mpi")
    depends_on("tbb", when="+tbb")
    depends_on("cuda", when="+cuda")

    depends_on("vtkm@master")
    depends_on("vtkm@master+tbb", when="+tbb")
    depends_on("vtkm@master+cuda", when="+cuda")

    def install(self, spec, prefix):
        with working_dir('spack-build', create=True):
            cmake_args = ["../src",
                          "-DVTKM_DIR={0}".format(spec["vtkm"].prefix),
                          "-DENABLE_TESTS=OFF",
                          "-DBUILD_TESTING=OFF"]
            # mpi support
            if "+mpi" in spec:
                mpicc = spec['mpi'].mpicc
                mpicxx = spec['mpi'].mpicxx
                cmake_args.extend(["-DMPI_C_COMPILER={0}".format(mpicc),
                                   "-DMPI_CXX_COMPILER={0}".format(mpicxx)])
                mpiexe_bin = join_path(spec['mpi'].prefix.bin, 'mpiexec')
                if os.path.isfile(mpiexe_bin):
                    cmake_args.append("-DMPIEXEC={0}".format(mpiexe_bin))
            # tbb support
            if "+tbb" in spec:
                cmake_args.append("-DTBB_DIR={0}".format(spec["tbb"].prefix))

            # cuda support
            if "+cuda" in spec:
                cmake_args.append("-DENABLE_CUDA=ON")
                # this fix is necessary if compiling platform has cuda, but
                # no devices (this common for front end nodes on hpc clusters)
                # we choose kepler as a lowest common denominator
                cmake_args.append("-DVTKm_CUDA_Architecture=kepler")

            # use release, instead of release with debug symbols b/c vtkh libs
            # can overwhelm compilers with too many symbols
            for arg in std_cmake_args:
                if arg.count("CMAKE_BUILD_TYPE") == 0:
                    cmake_args.extend(std_cmake_args)
            cmake_args.append("-DCMAKE_BUILD_TYPE=Release")
            cmake(*cmake_args)
            if "+cuda" in spec:
                # avoid issues with make -j and FindCuda deps
                # likely a ordering issue that needs to be resolved
                # in vtk-h
                make(parallel=False)
            else:
                make()
            make("install")
