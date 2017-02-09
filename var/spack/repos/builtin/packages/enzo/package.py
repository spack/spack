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
from llnl.util.filesystem import join_path
from llnl.util import tty
from spack.architecture import sys_type
from spack.package import InstallError
import os
from shutil import copy


class Enzo(Package):
    """The Enzo package provides the hydrodynamic code enzo"""

    homepage="http://enzo-project.org/"
    url="https://bitbucket.org/enzo/enzo-dev/get/enzo-2.5.tar.bz2"

    version("development", hg="https://bitbucket.org/enzo/enzo-dev")
    version("stable", hg="https://bitbucket.org/enzo/enzo-dev", revision='stable')
    version("2.5", "ede4a3a59cabf2cdb4a29c49f5bedb20")
    version("2.4", "ad296817307be83b3bc9fe9b0494df8a")
    version("2.3", "0b8a47117ef95fd561c3319e8992ddf9")
    version("2.2", "65fe5a8dced223753e02aaa9e3e92603")
    version("2.1.1", "0fe775d0a05d5e434b7d1c3e927146d2")
    version("2.1.0", "224a426312af03a573c2087b6d94a2d4")
    
    variant("warn", default=False, description="Warn compiling mode")
    variant("debug", default=False, description="Debug compiling mode")
    variant("high", default=True, description="High compiling mode")
    variant("aggressive", default=False, description="Aggressive compiling mode")

    depends_on('python@:2.7.999', type=('build'))
    depends_on('mercurial', type=('build'))
    depends_on('makedepend', type=('build'))
    depends_on('hdf5@1.8.16', type=('build', 'link', 'run'))
    depends_on('mpi', type=('build', 'link', 'run'))

    def install(self, spec, prefix):
        if ((('+warn' in spec) and ('+debug' in spec)) or
            (('+warn' in spec) and ('+high' in spec)) or
            (('+warn' in spec) and ('+aggressive' in spec)) or
            (('+debug' in spec) and ('+high' in spec)) or
            (('+debug' in spec) and ('+aggressive' in spec)) or
            (('+high' in spec) and ('+aggressive' in spec))):
            raise InstallError("Can only specify one of" 
                "+warn,+debug,+high,and+aggressive")

        build_option = ""
        if '+warn' in spec:
            build_option = 'opt-warn'
        elif '+debug' in spec:
            build_option = 'opt-debug'
        elif '+high' in spec:
            build_option = 'opt-high'
        elif '+aggressive' in spec:
            build_option = 'opt-aggressive'

        # destroy old bin
        if os.path.exists("bin"):
            rmtree("bin")
        mkdir("bin")
        
        # First run configure
        configure()
            
        # First, build enzo
        cd("src/enzo")

        tty.msg("Current directory is: %s" % os.getcwd())        

        # Remove configuration file
        if(os.path.exists("Make.mach.spack")):
            remove("Make.mach.spack")

        #Write configuration file
        build_config_file = open("Make.mach.spack", "w")
        build_config_file.write("""
#=======================================================================\n
#\n
# FILE:        Make.mach.spack\n
#\n
# DESCRIPTION: Makefile settings for a machine using spack\n
#\n
# AUTHOR:      Matthew Krafczyk (krafczyk.matthew@gmail.com)\n
#\n
# DATE:        2017-02-09\n
#\n
# This configuration is built with w/e is needed using spack\n
#\n
#=======================================================================\n
\n
MACH_TEXT  = Spack on %s\n
MACH_VALID = 1\n
MACH_FILE  = Make.mach.spack\n
\n
#-----------------------------------------------------------------------\n
# Install paths (local variables)\n
#-----------------------------------------------------------------------\n
\n
""" % sys_type())

        mpi_prefix = spec['mpi'].prefix
        hdf5_prefix = spec['hdf5'].prefix
        build_config_file.write("LOCAL_MPI_INSTALL = %s\n" % mpi_prefix)
        build_config_file.write("LOCAL_HDF5_INSTALL = %s\n" % hdf5_prefix)
        build_config_file.write("LOCAL_GRACKLE_INSTALL = /usr/local\n")

        build_config_file.write("""
\n
#-----------------------------------------------------------------------\n
# Compiler settings\n
#-----------------------------------------------------------------------\n
\n
MACH_CPP       = cpp # C preprocessor command\n
\n
# With MPI\n
\n
MACH_CC_MPI    = mpicc # C compiler when using MPI\n
MACH_CXX_MPI   = mpic++ # C++ compiler when using MPI\n
MACH_FC_MPI    = gfortran # Fortran 77 compiler when using MPI\n
MACH_F90_MPI   = gfortran # Fortran 90 compiler when using MPI\n
MACH_LD_MPI    = mpic++ # Linker when using MPI\n
\n
# Without MPI\n
\n
MACH_CC_NOMPI  = gcc # C compiler when not using MPI\n
MACH_CXX_NOMPI = g++ # C++ compiler when not using MPI\n
MACH_FC_NOMPI  = gfortran # Fortran 77 compiler when not using MPI\n
MACH_F90_NOMPI = gfortran # Fortran 90 compiler when not using MPI\n
MACH_LD_NOMPI  = g++ # Linker when not using MPI\n
\n
#-----------------------------------------------------------------------\n
# Machine-dependent defines\n
#-----------------------------------------------------------------------\n
\n
MACH_DEFINES   = -DLINUX -DH5_USE_16_API \n
\n
#-----------------------------------------------------------------------\n
# Compiler flag settings\n
#-----------------------------------------------------------------------\n
\n
\n
MACH_CPPFLAGS = -P -traditional \n
MACH_CFLAGS   = \n
MACH_CXXFLAGS = -DMPICH_IGNORE_CXX_SEEK -DMPICH_SKIP_MPICXX\n
MACH_FFLAGS   = -fno-second-underscore -ffixed-line-length-132\n
MACH_F90FLAGS = -fno-second-underscore\n
MACH_LDFLAGS  = \n
\n
#-----------------------------------------------------------------------\n
# Optimization flags\n
#-----------------------------------------------------------------------\n
\n
MACH_OPT_WARN        = -Wall -g\n
MACH_OPT_DEBUG       = -g\n
MACH_OPT_HIGH        = -O2\n
MACH_OPT_AGGRESSIVE  = -O3 -g\n
\n
#-----------------------------------------------------------------------\n
# Includes\n
#-----------------------------------------------------------------------\n
\n
LOCAL_INCLUDES_MPI    = -I$(LOCAL_MPI_INSTALL)/include # MPI includes\n
LOCAL_INCLUDES_HDF5   = -I$(LOCAL_HDF5_INSTALL)/include # HDF5 includes\n
LOCAL_INCLUDES_HYPRE  = # hypre includes\n
LOCAL_INCLUDES_PAPI   = # PAPI includes\n
LOCAL_INCLUDES_GRACKLE = -I$(LOCAL_GRACKLE_INSTALL)/include\n
\n
MACH_INCLUDES         = $(LOCAL_INCLUDES_MPI) $(LOCAL_INCLUDES_HDF5)\n
MACH_INCLUDES_MPI     = $(LOCAL_INCLUDES_MPI)\n
MACH_INCLUDES_HYPRE   = $(LOCAL_INCLUDES_HYPRE)\n
MACH_INCLUDES_PAPI    = $(LOCAL_INCLUDES_PAPI)\n
MACH_INCLUDES_GRACKLE  = $(LOCAL_INCLUDES_GRACKLE)\n
\n
#-----------------------------------------------------------------------\n
# Libraries\n
#-----------------------------------------------------------------------\n
\n
LOCAL_LIBS_MPI    = -L$(LOCAL_MPI_INSTALL)/lib -lmpi -lmpicxx # MPI libraries\n
LOCAL_LIBS_HDF5   = -L$(LOCAL_HDF5_INSTALL)/lib -lhdf5 -lz # HDF5 libraries\n
LOCAL_LIBS_HYPRE  = # hypre libraries\n
LOCAL_LIBS_PAPI   = # PAPI libraries\n
LOCAL_LIBS_MACH   = -lgfortran # Machine-dependent libraries\n
LOCAL_LIBS_GRACKLE = -L$(LOCAL_GRACKLE_INSTALL)/lib -lgrackle\n
\n
MACH_LIBS         = $(LOCAL_LIBS_HDF5) $(LOCAL_LIBS_MACH)\n
MACH_LIBS_MPI     = $(LOCAL_LIBS_MPI)\n
MACH_LIBS_HYPRE   = $(LOCAL_LIBS_HYPRE)\n
MACH_LIBS_PAPI    = $(LOCAL_LIBS_PAPI)\n
MACH_LIBS_GRACKLE = $(LOCAL_LIBS_GRACKLE)\n""")
        build_config_file.close()

        # Set machine options
        make("machine-spack")
        # Set debug mode
        make(build_option)
        make("clean")
        # Build
        make()

        # Now for the inits tool
        cd("../inits")
        make("machine-spack")
        make("clean")
        make(build_option)
        make()

        # And the ring tool
        cd("../ring")
        make("machine-spack")
        make(build_option)
        make("clean")
        make()
        copy('ring.exe', '../../bin/ring')

        cd("../..")
        # Install results
        mkdirp(join_path(prefix, "bin"))
        for item in os.listdir("bin"):
            install("bin/%s" % item, join_path(prefix, "bin/%s" % item))
