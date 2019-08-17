# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack import *

import sys
import os
import socket


import llnl.util.tty as tty
from os import environ as env


def cmake_cache_entry(name, value, vtype=None):
    """
    Helper that creates CMake cache entry strings used in
    'host-config' files.
    """
    if vtype is None:
        if value == "ON" or value == "OFF":
            vtype = "BOOL"
        else:
            vtype = "PATH"
    return 'set({0} "{1}" CACHE {2} "")\n\n'.format(name, value, vtype)


class Vtkh(Package):
    """VTK-h is a toolkit of scientific visualization algorithms for emerging
    processor architectures. VTK-h brings together several projects like VTK-m
    and DIY2 to provide a toolkit with hybrid parallel capabilities."""

    homepage = "https://github.com/Alpine-DAV/vtk-h"
    git      = "https://github.com/Alpine-DAV/vtk-h.git"
    maintainers = ['cyrush']

    version('develop', branch='develop', submodules=True)
    version('0.1.0', branch='develop', tag='v0.1.0', submodules=True)

    variant("shared", default=True, description="Build vtk-h as shared libs")
    variant("mpi", default=True, description="build mpi support")
    variant("tbb", default=False, description="build tbb support")
    variant("cuda", default=False, description="build cuda support")
    variant("openmp", default=(sys.platform != 'darwin'),
            description="build openmp support")

    depends_on("cmake@3.8.2:", type='build')

    depends_on("mpi", when="+mpi")
    depends_on("intel-tbb", when="@0.1.0+tbb")
    depends_on("cuda", when="+cuda")

    depends_on("vtkm@1.2.0", when="@0.1.0")
    depends_on("vtkm@1.2.0+tbb", when="@0.1.0+tbb")
    depends_on("vtkm@1.2.0+cuda", when="@0.1.0+cuda")
    depends_on("vtkm@1.2.0~shared", when="@0.1.0~shared")

    depends_on("vtkm@master~tbb+openmp", when="@develop+openmp")
    depends_on("vtkm@master~tbb~openmp", when="@develop~openmp")

    depends_on("vtkm@master+cuda~tbb+openmp", when="@develop+cuda+openmp")
    depends_on("vtkm@master+cuda~tbb~openmp", when="@develop+cuda~openmp")

    depends_on("vtkm@master~tbb+openmp~shared", when="@develop+openmp~shared")
    depends_on("vtkm@master~tbb~openmp~shared", when="@develop~openmp~shared")

    depends_on("vtkm@master+cuda~tbb+openmp~shared", when="@develop+cuda+openmp~shared")
    depends_on("vtkm@master+cuda~tbb~openmp~shared", when="@develop+cuda~openmp~shared")

    patch('vtkm_lagrange_cuda_fix.patch')

    def install(self, spec, prefix):
        with working_dir('spack-build', create=True):
            cmake_args = ["../src",
                          "-DVTKM_DIR={0}".format(spec["vtkm"].prefix),
                          "-DENABLE_TESTS=OFF",
                          "-DBUILD_TESTING=OFF"]

            # shared vs static libs
            if "+shared" in spec:
                cmake_args.append('-DBUILD_SHARED_LIBS=ON')
            else:
                cmake_args.append('-DBUILD_SHARED_LIBS=OFF')

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

            # openmp support
            if "+openmp" in spec:
                cmake_args.append("-DENABLE_OPENMP=ON")

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

    def create_host_config(self, spec, prefix, py_site_pkgs_dir=None):
        """
        This method creates a 'host-config' file that specifies
        all of the options used to configure and build vtkh.
        """

        #######################
        # Compiler Info
        #######################
        c_compiler = env["SPACK_CC"]
        cpp_compiler = env["SPACK_CXX"]

        #######################################################################
        # By directly fetching the names of the actual compilers we appear
        # to doing something evil here, but this is necessary to create a
        # 'host config' file that works outside of the spack install env.
        #######################################################################

        sys_type = spec.architecture
        # if on llnl systems, we can use the SYS_TYPE
        if "SYS_TYPE" in env:
            sys_type = env["SYS_TYPE"]

        ##############################################
        # Find and record what CMake is used
        ##############################################

        cmake_exe = spec['cmake'].command.path

        host_cfg_fname = "%s-%s-%s-vtkh.cmake" % (socket.gethostname(),
                                                  sys_type,
                                                  spec.compiler)

        cfg = open(host_cfg_fname, "w")
        cfg.write("##################################\n")
        cfg.write("# spack generated host-config\n")
        cfg.write("##################################\n")
        cfg.write("# {0}-{1}\n".format(sys_type, spec.compiler))
        cfg.write("##################################\n\n")

        # Include path to cmake for reference
        cfg.write("# cmake from spack \n")
        cfg.write("# cmake executable path: %s\n\n" % cmake_exe)

        #######################
        # Compiler Settings
        #######################

        cfg.write("#######\n")
        cfg.write("# using %s compiler spec\n" % spec.compiler)
        cfg.write("#######\n\n")
        cfg.write("# c compiler used by spack\n")
        cfg.write(cmake_cache_entry("CMAKE_C_COMPILER", c_compiler))
        cfg.write("# cpp compiler used by spack\n")
        cfg.write(cmake_cache_entry("CMAKE_CXX_COMPILER", cpp_compiler))

        # shared vs static libs
        if "+shared" in spec:
            cfg.write(cmake_cache_entry("BUILD_SHARED_LIBS", "ON"))
        else:
            cfg.write(cmake_cache_entry("BUILD_SHARED_LIBS", "OFF"))

        #######################################################################
        # Core Dependencies
        #######################################################################

        #######################
        # VTK-h (and deps)
        #######################

        cfg.write("# vtk-m support \n")

        if "+openmp" in spec:
            cfg.write("# enable openmp support\n")
            cfg.write(cmake_cache_entry("ENABLE_OPENMP", "ON"))

        cfg.write("# vtk-m from spack\n")
        cfg.write(cmake_cache_entry("VTKM_DIR", spec['vtkm'].prefix))

        #######################################################################
        # Optional Dependencies
        #######################################################################

        #######################
        # MPI
        #######################

        cfg.write("# MPI Support\n")

        if "+mpi" in spec:
            cfg.write(cmake_cache_entry("ENABLE_MPI", "ON"))
            cfg.write(cmake_cache_entry("MPI_C_COMPILER", spec['mpi'].mpicc))
            cfg.write(cmake_cache_entry("MPI_CXX_COMPILER",
                                        spec['mpi'].mpicxx))
            cfg.write(cmake_cache_entry("MPI_Fortran_COMPILER",
                                        spec['mpi'].mpifc))
            mpiexe_bin = join_path(spec['mpi'].prefix.bin, 'mpiexec')
            if os.path.isfile(mpiexe_bin):
                # starting with cmake 3.10, FindMPI expects MPIEXEC_EXECUTABLE
                # vs the older versions which expect MPIEXEC
                if self.spec["cmake"].satisfies('@3.10:'):
                    cfg.write(cmake_cache_entry("MPIEXEC_EXECUTABLE",
                                                mpiexe_bin))
                else:
                    cfg.write(cmake_cache_entry("MPIEXEC",
                                                mpiexe_bin))
        else:
            cfg.write(cmake_cache_entry("ENABLE_MPI", "OFF"))

        #######################
        # CUDA
        #######################

        cfg.write("# CUDA Support\n")

        if "+cuda" in spec:
            cfg.write(cmake_cache_entry("ENABLE_CUDA", "ON"))
        else:
            cfg.write(cmake_cache_entry("ENABLE_CUDA", "OFF"))

        cfg.write("##################################\n")
        cfg.write("# end spack generated host-config\n")
        cfg.write("##################################\n")
        cfg.close()

        host_cfg_fname = os.path.abspath(host_cfg_fname)
        tty.info("spack generated conduit host-config file: " + host_cfg_fname)
        return host_cfg_fname
