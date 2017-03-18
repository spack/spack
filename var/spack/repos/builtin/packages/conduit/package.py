##############################################################################
# Copyright (c) 2013-2016, Lawrence Livermore National Security, LLC.
# Produced at the Lawrence Livermore National Laboratory.
#
# This file is part of Spack.
# Created by Todd Gamblin, tgamblin@llnl.gov, All rights reserved.
# LLNL-CODE-647188
#
# For details, see https://github.com/llnl/spack
# Please also see the LICENSE file for our notice and the LGPL.
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

import socket
import os

import llnl.util.tty as tty


def cmake_cache_entry(name, value):
    """
    Helper that creates CMake cache entry strings used in
    'host-config' files.
    """
    return 'set("{0}" "{1}" CACHE PATH "")\n\n'.format(name, value)


class Conduit(Package):
    """Conduit is an open source project from Lawrence Livermore National
    Laboratory that provides an intuitive model for describing hierarchical
    scientific data in C++, C, Fortran, and Python. It is used for data
    coupling between packages in-core, serialization, and I/O tasks."""

    homepage = "http://software.llnl.gov/conduit"
    url = "https://github.com/LLNL/conduit/archive/v0.2.1.tar.gz"

    version('0.2.1', 'cd2b42c76f70ac3546582b6da77c6028')
    version('0.2.0', 'd595573dedf55514c11d7391092fd760')

    version('master', git='https://github.com/LLNL/conduit.git')

    ###########################################################################
    # package variants
    ###########################################################################

    variant("shared", default=True, description="Build Conduit as shared libs")

    variant("cmake", default=True,
            description="Build CMake (if off, attempt to use cmake from PATH)")

    # variants for python support
    variant("python", default=True, description="Build Conduit Python support")

    # variants for comm and i/o
    variant("mpi", default=True, description="Build Conduit MPI Support")
    variant("hdf5", default=True, description="Build Conduit HDF5 support")
    variant("silo", default=True, description="Build Conduit Silo support")

    # variants for dev-tools (docs, etc)
    variant("doc", default=False, description="Build Conduit's documentation")

    ###########################################################################
    # package dependencies
    ###########################################################################

    #######################
    # CMake
    #######################
    # cmake 3.3.1 is the version we tested
    depends_on("cmake@3.3.1", when="+cmake")

    #######################
    # Python
    #######################
    extends("python", when="+python")
    # TODO: blas and lapack are disabled due to build
    # issues Cyrus experienced on OSX 10.11.6
    depends_on("py-numpy~blas~lapack", when="+python", type=('build', 'run'))

    #######################
    # I/O Packages
    #######################
    # TODO: cxx variant is disabled due to build issue Cyrus
    # experienced on BGQ. When on, the static build tries
    # to link agains shared libs.
    #
    # we are not using hdf5's mpi or fortran features.
    depends_on("hdf5~cxx~mpi~fortran", when="+shared")
    depends_on("hdf5~shared~cxx~mpi~fortran", when="~shared")

    # we are not using silo's fortran features
    depends_on("silo~fortran", when="+shared")
    depends_on("silo~shared~fortran", when="~shared")

    #######################
    # MPI
    #######################
    depends_on("mpi", when="+mpi")

    #######################
    # Documentation related
    #######################
    depends_on("py-sphinx", when="+python+doc", type='build')
    depends_on("doxygen", when="+doc")

    def install(self, spec, prefix):
        """
        Build and install Conduit.
        """
        with working_dir('spack-build', create=True):
            host_cfg_fname = self.create_host_config(spec, prefix)
            cmake_args = []
            # if we have a static build, we need to avoid any of
            # spack's default cmake settings related to rpaths
            # (see: https://github.com/LLNL/spack/issues/2658)
            if "+shared" in spec:
                cmake_args.extend(std_cmake_args)
            else:
                for arg in std_cmake_args:
                    if arg.count("RPATH") == 0:
                        cmake_args.append(arg)
            cmake_args.extend(["-C", host_cfg_fname, "../src"])
            cmake(*cmake_args)
            make()
            make("install")

    def create_host_config(self, spec, prefix):
        """
        This method creates a 'host-config' file that specifies
        all of the options used to configure and build conduit.

        For more details see about 'host-config' files see:
            http://software.llnl.gov/conduit/building.html
        """

        #######################
        # Compiler Info
        #######################
        c_compiler = env["SPACK_CC"]
        cpp_compiler = env["SPACK_CXX"]
        f_compiler = None

        if self.compiler.fc:
            # even if this is set, it may not exist so do one more sanity check
            if os.path.isfile(env["SPACK_FC"]):
                f_compiler = env["SPACK_FC"]

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

        if "+cmake" in spec:
            cmake_exe = join_path(spec['cmake'].prefix.bin, "cmake")
        else:
            cmake_exe = which("cmake")
            if cmake_exe is None:
                msg = 'failed to find CMake (and cmake variant is off)'
                raise RuntimeError(msg)
            cmake_exe = cmake_exe.command

        host_cfg_fname = "%s-%s-%s.cmake" % (socket.gethostname(),
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

        cfg.write("# fortran compiler used by spack\n")
        if f_compiler is not None:
            cfg.write(cmake_cache_entry("ENABLE_FORTRAN", "ON"))
            cfg.write(cmake_cache_entry("CMAKE_Fortran_COMPILER", f_compiler))
        else:
            cfg.write("# no fortran compiler found\n\n")
            cfg.write(cmake_cache_entry("ENABLE_FORTRAN", "OFF"))

        #######################
        # Python
        #######################

        cfg.write("# Python Support\n")

        if "+python" in spec:
            python_exe = join_path(spec['python'].prefix.bin, "python")
            cfg.write("# Enable python module builds\n")
            cfg.write(cmake_cache_entry("ENABLE_PYTHON", "ON"))
            cfg.write("# python from spack \n")
            cfg.write(cmake_cache_entry("PYTHON_EXECUTABLE", python_exe))
            # install module to standard style site packages dir
            # so we can support spack activate
            py_ver_short = "python{0}".format(spec["python"].version.up_to(2))
            pym_prefix = join_path("${CMAKE_INSTALL_PREFIX}",
                                   "lib",
                                   py_ver_short,
                                   "site-packages")
            # use pym_prefix as the install path
            cfg.write(cmake_cache_entry("PYTHON_MODULE_INSTALL_PREFIX",
                                        pym_prefix))
        else:
            cfg.write(cmake_cache_entry("ENABLE_PYTHON", "OFF"))

        if "+doc" in spec:
            cfg.write(cmake_cache_entry("ENABLE_DOCS", "ON"))

            cfg.write("# sphinx from spack \n")
            sphinx_build_exe = join_path(spec['py-sphinx'].prefix.bin,
                                         "sphinx-build")
            cfg.write(cmake_cache_entry("SPHINX_EXECUTABLE", sphinx_build_exe))

            cfg.write("# doxygen from uberenv\n")
            doxygen_exe = join_path(spec['doxygen'].prefix.bin, "doxygen")
            cfg.write(cmake_cache_entry("DOXYGEN_EXECUTABLE", doxygen_exe))
        else:
            cfg.write(cmake_cache_entry("ENABLE_DOCS", "OFF"))

        #######################
        # MPI
        #######################

        cfg.write("# MPI Support\n")

        if "+mpi" in spec:
            cfg.write(cmake_cache_entry("ENABLE_MPI", "ON"))
            cfg.write(cmake_cache_entry("MPI_C_COMPILER", spec['mpi'].mpicc))
            # we use `mpicc` as `MPI_CXX_COMPILER` b/c we don't want to
            # introduce linking deps to the MPI C++ libs (we aren't using
            # C++ features of MPI) -- this happens with some versions of
            # OpenMPI
            cfg.write(cmake_cache_entry("MPI_CXX_COMPILER", spec['mpi'].mpicc))
            cfg.write(cmake_cache_entry("MPI_Fortran_COMPILER",
                                        spec['mpi'].mpifc))
        else:
            cfg.write(cmake_cache_entry("ENABLE_MPI", "OFF"))

        #######################################################################
        # I/O Packages
        #######################################################################

        cfg.write("# I/O Packages\n\n")

        #######################
        # HDF5
        #######################

        cfg.write("# hdf5 from spack \n")

        if "+hdf5" in spec:
            cfg.write(cmake_cache_entry("HDF5_DIR", spec['hdf5'].prefix))
        else:
            cfg.write("# hdf5 not built by spack \n")

        #######################
        # Silo
        #######################

        cfg.write("# silo from spack \n")

        if "+silo" in spec:
            cfg.write(cmake_cache_entry("SILO_DIR", spec['silo'].prefix))
        else:
            cfg.write("# silo not built by spack \n")

        cfg.write("##################################\n")
        cfg.write("# end spack generated host-config\n")
        cfg.write("##################################\n")
        cfg.close()

        host_cfg_fname = os.path.abspath(host_cfg_fname)
        tty.info("spack generated conduit host-config file: " + host_cfg_fname)
        return host_cfg_fname
