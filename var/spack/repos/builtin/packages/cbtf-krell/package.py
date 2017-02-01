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
##########################################################################
# Copyright (c) 2015-2016 Krell Institute. All Rights Reserved.
#
# This program is free software; you can redistribute it and/or modify it under
# the terms of the GNU General Public License as published by the Free Software
# Foundation; either version 2 of the License, or (at your option) any later
# version.
#
# This program is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
# FOR A PARTICULAR PURPOSE.  See the GNU General Public License for more
# details.
#
# You should have received a copy of the GNU General Public License along with
# this program; if not, write to the Free Software Foundation, Inc., 59 Temple
# Place, Suite 330, Boston, MA  02111-1307  USA
##########################################################################

from spack import *


class CbtfKrell(Package):
    """CBTF Krell project contains the Krell Institute contributions to the
       CBTF project.  These contributions include many performance data
       collectors and support libraries as well as some example tools
       that drive the data collection at HPC levels of scale.

    """
    homepage = "http://sourceforge.net/p/cbtf/wiki/Home/"

    # optional mirror access template
    # url      = "file:/home/jeg/cbtf-krell-1.6.tar.gz"
    # version('1.6', 'edeb61cd488f16e7b124f77db9ce762d')

    version('1.8', branch='master',
            git='https://github.com/OpenSpeedShop/cbtf-krell.git')

    # MPI variants
    variant('openmpi', default=False,
            description="Build mpi experiment collector for openmpi MPI..")
    variant('mpt', default=False,
            description="Build mpi experiment collector for SGI MPT MPI.")
    variant('mvapich2', default=False,
            description="Build mpi experiment collector for mvapich2 MPI.")
    variant('mvapich', default=False,
            description="Build mpi experiment collector for mvapich MPI.")
    variant('mpich2', default=False,
            description="Build mpi experiment collector for mpich2 MPI.")
    variant('mpich', default=False,
            description="Build mpi experiment collector for mpich MPI.")

    # Dependencies for cbtf-krell
    depends_on("cmake@3.0.2:", type='build')

    # For binutils service
    depends_on("binutils@2.24+krellpatch")

    # collectionTool
    depends_on("boost@1.50.0:1.59.0")
    depends_on("dyninst@9.2.0")
    depends_on("mrnet@5.0.1:+lwthreads")

    depends_on("xerces-c@3.1.1:")
    depends_on("cbtf")

    # for services and collectors
    depends_on("libmonitor+krellpatch")
    depends_on("libunwind")
    depends_on("papi")

    # MPI Installations
    # These have not worked either for build or execution, commenting out for
    # now
    depends_on("openmpi", when='+openmpi')
    depends_on("mpich", when='+mpich')
    depends_on("mpich2", when='+mpich2')
    depends_on("mvapich2", when='+mvapich2')
    depends_on("mvapich", when='+mvapich')
    depends_on("mpt", when='+mpt')

    parallel = False

    def adjustBuildTypeParams_cmakeOptions(self, spec, cmakeOptions):
        # Sets build type parameters into cmakeOptions the options that will
        # enable the cbtf-krell built type settings

        compile_flags = "-O2 -g"
        BuildTypeOptions = []
        # Set CMAKE_BUILD_TYPE to what cbtf-krell wants it to be, not the
        # stdcmakeargs
        for word in cmakeOptions[:]:
            if word.startswith('-DCMAKE_BUILD_TYPE'):
                cmakeOptions.remove(word)
            if word.startswith('-DCMAKE_CXX_FLAGS'):
                cmakeOptions.remove(word)
            if word.startswith('-DCMAKE_C_FLAGS'):
                cmakeOptions.remove(word)
            if word.startswith('-DCMAKE_VERBOSE_MAKEFILE'):
                cmakeOptions.remove(word)
        BuildTypeOptions.extend([
            '-DCMAKE_VERBOSE_MAKEFILE=ON',
            '-DCMAKE_BUILD_TYPE=None',
            '-DCMAKE_CXX_FLAGS=%s'         % compile_flags,
            '-DCMAKE_C_FLAGS=%s'           % compile_flags
        ])

        cmakeOptions.extend(BuildTypeOptions)

    def set_mpi_cmakeOptions(self, spec, cmakeOptions):
        # Appends to cmakeOptions the options that will enable the appropriate
        # MPI implementations

        MPIOptions = []

        # openmpi
        if '+openmpi' in spec:
            MPIOptions.append('-DOPENMPI_DIR=%s' % spec['openmpi'].prefix)
        # mpich
        if '+mpich' in spec:
            MPIOptions.append('-DMPICH_DIR=%s' % spec['mpich'].prefix)
        # mpich2
        if '+mpich2' in spec:
            MPIOptions.append('-DMPICH2_DIR=%s' % spec['mpich2'].prefix)
        # mvapich
        if '+mvapich' in spec:
            MPIOptions.append('-DMVAPICH_DIR=%s' % spec['mvapich'].prefix)
        # mvapich2
        if '+mvapich2' in spec:
            MPIOptions.append('-DMVAPICH2_DIR=%s' % spec['mvapich2'].prefix)
        # mpt
        if '+mpt' in spec:
            MPIOptions.append('-DMPT_DIR=%s' % spec['mpt'].prefix)

        cmakeOptions.extend(MPIOptions)

    def install(self, spec, prefix):

        # Add in paths for finding package config files that tell us
        # where to find these packages
        # cmake_prefix_path = \
        #     join_path(spec['cbtf'].prefix) + ':' + \
        #     join_path(spec['dyninst'].prefix)
        # '-DCMAKE_PREFIX_PATH=%s' % cmake_prefix_path

        # Build cbtf-krell with cmake
        with working_dir('build_cbtf_krell', create=True):
            cmakeOptions = []
            cmakeOptions.extend(
                ['-DCMAKE_INSTALL_PREFIX=%s' % prefix,
                 '-DCBTF_DIR=%s' % spec['cbtf'].prefix,
                 '-DBINUTILS_DIR=%s' % spec['binutils'].prefix,
                 '-DLIBMONITOR_DIR=%s' % spec['libmonitor'].prefix,
                 '-DLIBUNWIND_DIR=%s' % spec['libunwind'].prefix,
                 '-DPAPI_DIR=%s' % spec['papi'].prefix,
                 '-DBOOST_DIR=%s' % spec['boost'].prefix,
                 '-DMRNET_DIR=%s' % spec['mrnet'].prefix,
                 '-DDYNINST_DIR=%s' % spec['dyninst'].prefix,
                 '-DXERCESC_DIR=%s' % spec['xerces-c'].prefix])

            # Add any MPI implementations coming from variant settings
            self.set_mpi_cmakeOptions(spec, cmakeOptions)

            # Add in the standard cmake arguments
            cmakeOptions.extend(std_cmake_args)

            # Adjust the standard cmake arguments to what we want the build
            # type, etc to be
            self.adjustBuildTypeParams_cmakeOptions(spec, cmakeOptions)

            # Invoke cmake
            cmake('..', *cmakeOptions)

            make("clean")
            make()
            make("install")

        # if '+cray' in spec:
        # if 'cray' in self.spec.architecture:
        #    if '+runtime' in spec:
        #        with working_dir('build_cbtf_cray_runtime', create=True):
        #            python_vers='%d.%d' % spec['python'].version[:2]
        #            cmake .. \
        #                -DCMAKE_BUILD_TYPE=Debug \
        #                -DTARGET_OS="cray" \
        #                -DRUNTIME_ONLY="true" \
        #                -DCMAKE_INSTALL_PREFIX=${CBTF_KRELL_PREFIX} \
        #                -DCMAKE_PREFIX_PATH=${CBTF_ROOT} \
        #                -DCBTF_DIR=${CBTF_ROOT} \
        #                -DBOOST_ROOT=${BOOST_INSTALL_PREFIX} \
        #                -DXERCESC_DIR=${XERCESC_INSTALL_PREFIX} \
        #                -DBINUTILS_DIR=${KRELL_ROOT} \
        #                -DLIBMONITOR_DIR=${KRELL_ROOT_COMPUTE} \
        #                -DLIBUNWIND_DIR=${KRELL_ROOT_COMPUTE} \
        #                -DPAPI_DIR=${PAPI_ROOT} \
        #                -DDYNINST_DIR=${DYNINST_CN_ROOT} \
        #                -DMRNET_DIR=${MRNET_INSTALL_PREFIX} \
        #                -DMPICH2_DIR=/opt/cray/mpt/7.0.1/gni/mpich2-gnu/48
        #    else:
        #        with working_dir('build_cbtf_cray_frontend', create=True):
        #            python_vers='%d.%d' % spec['python'].version[:2]
        #            cmake .. \
        #            -DCMAKE_BUILD_TYPE=Debug \
        #            -DCMAKE_INSTALL_PREFIX=${CBTF_KRELL_PREFIX} \
        #            -DCMAKE_PREFIX_PATH=${CBTF_ROOT} \
        #            -DCBTF_DIR=${CBTF_ROOT} \
        #            -DRUNTIME_TARGET_OS="cray" \
        #          -DCBTF_KRELL_CN_RUNTIME_DIR=${CBTF_KRELL_CN_RUNTIME_ROOT} \
        #            -DCBTF_CN_RUNTIME_DIR=${CBTF_CN_RUNTIME_ROOT} \
        #            -DLIBMONITOR_CN_RUNTIME_DIR=${LIBMONITOR_CN_ROOT} \
        #            -DLIBUNWIND_CN_RUNTIME_DIR=${LIBUNWIND_CN_ROOT} \
        #            -DPAPI_CN_RUNTIME_DIR=${PAPI_CN_ROOT} \
        #            -DXERCESC_CN_RUNTIME_DIR=/${XERCESC_CN_ROOT} \
        #            -DMRNET_CN_RUNTIME_DIR=${MRNET_CN_ROOT} \
        #            -DBOOST_CN_RUNTIME_DIR=${BOOST_CN_ROOT} \
        #            -DDYNINST_CN_RUNTIME_DIR=${DYNINST_CN_ROOT} \
        #            -DBOOST_ROOT=/${KRELL_ROOT} \
        #            -DXERCESC_DIR=/${KRELL_ROOT} \
        #            -DBINUTILS_DIR=/${KRELL_ROOT} \
        #            -DLIBMONITOR_DIR=${KRELL_ROOT} \
        #            -DLIBUNWIND_DIR=${KRELL_ROOT} \
        #            -DPAPI_DIR=${PAPI_ROOT} \
        #            -DDYNINST_DIR=${KRELL_ROOT} \
        #            -DMRNET_DIR=${KRELL_ROOT} \
        #            -DMPICH2_DIR=/opt/cray/mpt/7.0.1/gni/mpich2-gnu/48
        #    fi
#
#                    make("clean")
#                    make()
#                    make("install")
#
#        elif '+mic' in spec:
#            if '+runtime' in spec:
#                with working_dir('build_cbtf_mic_runtime', create=True):
#                    python_vers='%d.%d' % spec['python'].version[:2]
#                    cmake .. \
#
#            else:
#                with working_dir('build_cbtf_cray_frontend', create=True):
#                    python_vers='%d.%d' % spec['python'].version[:2]
#                    cmake .. \
#            fi
#
#        else:
#            # Build cbtf-krell with cmake
#            with working_dir('build_cbtf_krell', create=True):
#                cmake('..',
#                      '-DCMAKE_BUILD_TYPE=Debug',
#                      '-DCMAKE_INSTALL_PREFIX=%s' % prefix,
#                      '-DCBTF_DIR=%s' % spec['cbtf'].prefix,
#                      '-DBINUTILS_DIR=%s' % spec['binutils'].prefix,
#                      '-DLIBMONITOR_DIR=%s' % spec['libmonitor'].prefix,
#                      '-DLIBUNWIND_DIR=%s'% spec['libunwind'].prefix,
#                      '-DPAPI_DIR=%s' % spec['papi'].prefix,
#                      '-DBOOST_DIR=%s' % spec['boost'].prefix,
#                      '-DMRNET_DIR=%s' % spec['mrnet'].prefix,
#                      '-DDYNINST_DIR=%s' % spec['dyninst'].prefix,
#                      '-DXERCESC_DIR=%s' % spec['xerces-c'].prefix,
#                      '-DOPENMPI_DIR=%s' % openmpi_prefix_path,
#                      '-DCMAKE_PREFIX_PATH=%s' % cmake_prefix_path,
#                      *std_cmake_args)
#
#                make("clean")
#                make()
#                make("install")
#
#        fi
#
