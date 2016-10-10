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
################################################################################
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
################################################################################

from spack import *
import os
import os.path

class Openspeedshop(Package):
    """OpenSpeedShop is a community effort by The Krell Institute with current direct funding from DOEs NNSA.
    It builds on top of a broad list of community infrastructures, most notably Dyninst and MRNet from UW,
    libmonitor from Rice, and PAPI from UTK. OpenSpeedShop is an open source multi platform Linux performance
    tool which is targeted to support performance analysis of applications running on both single node and
    large scale IA64, IA32, EM64T, AMD64, PPC, ARM, Blue Gene and Cray platforms.  OpenSpeedShop development
    is hosted by the Krell Institute. The infrastructure and base components of OpenSpeedShop are released
    as open source code primarily under LGPL.
    """

    homepage = "http://www.openspeedshop.org"
    url		= "https://github.com/OpenSpeedShop"
    version('2.2', '16cb051179c2038de4e8a845edf1d573')
    # Use when the git repository is available
    version('2.2', branch='master', git='https://github.com/OpenSpeedShop/openspeedshop.git')

    # Optional mirror template
    #url = "file:/home/jeg/OpenSpeedShop_ROOT/SOURCES/openspeedshop-2.2.tar.gz"
    #version('2.2', '517a7798507241ad8abd8b0626a4d2cf')

    parallel = False

    variant('offline', default=False, description="build with offline instrumentor enabled.")
    variant('cbtf', default=True, description="build with cbtf instrumentor enabled.")
    variant('runtime', default=False, description="build only the runtime libraries and collectors.")
    variant('frontend', default=False, description="build only the front-end tool using the runtime_dir to point to the target build.")
    variant('cuda', default=False, description="build with cuda packages included.")
    variant('ptgf', default=False, description="build with the PTGF based gui package enabled.")
    variant('rtfe', default=False, description="build for generic cluster platforms that have different processors on the fe and be nodes.")

    # MPI variants
    variant('openmpi', default=False, description="Build mpi experiment collector for openmpi MPI when this variant is enabled.")
    variant('mpt', default=False, description="Build mpi experiment collector for SGI MPT MPI when this variant is enabled.")
    variant('mvapich2', default=False, description="Build mpi experiment collector for mvapich2 MPI when this variant is enabled.")
    variant('mvapich', default=False, description="Build mpi experiment collector for mvapich MPI when this variant is enabled.")
    variant('mpich2', default=False, description="Build mpi experiment collector for mpich2 MPI when this variant is enabled.")
    variant('mpich', default=False, description="Build mpi experiment collector for mpich MPI when this variant is enabled.")

    depends_on("cmake@3.0.2:", type='build')
    # Dependencies for openspeedshop that are common to all the variants of the OpenSpeedShop build
    depends_on("bison", type='build')
    depends_on("flex", type='build')
    depends_on("binutils@2.24+krellpatch", type='build')
    depends_on("libelf")
    depends_on("libdwarf")
    depends_on("sqlite")
    depends_on("boost@1.50.0:")
    #depends_on("boost@1.53.0")
    depends_on("dyninst@9.1.0:")
    depends_on("python")
    depends_on("qt@3.3.8b+krellpatch")

    # Dependencies only for the openspeedshop offline package.
    depends_on("libunwind", when='+offline')
    depends_on("papi", when='+offline')
    depends_on("libmonitor+krellpatch", when='+offline')
    depends_on("openmpi", when='+offline+openmpi')
    depends_on("mpich", when='+offline+mpich')
    depends_on("mpich2", when='+offline+mpich2')
    depends_on("mvapich2", when='+offline+mvapich2')
    depends_on("mvapich", when='+offline+mvapich')
    depends_on("mpt", when='+offline+mpt')

    # Dependencies only for the openspeedshop cbtf package.
    depends_on("cbtf", when='+cbtf')
    depends_on("cbtf-krell", when='+cbtf')
    depends_on("cbtf-argonavis", when='+cbtf+cuda')
    depends_on("mrnet@5.0.1:+lwthreads", when='+cbtf')
    # We don't need this for building, but to complete the runtime module file
    # It is required in cbtf, so it will be available and not cause another rebuild
    depends_on("xerces-c@3.1.1:", when='+cbtf')

    def adjustBuildTypeParams_cmakeOptions(self, spec, cmakeOptions):
        # Sets build type parameters into cmakeOptions the options that will enable the cbtf-krell built type settings

        compile_flags="-O2 -g"
        BuildTypeOptions = []
        # Set CMAKE_BUILD_TYPE to what cbtf-krell wants it to be, not the stdcmakeargs
        for word in cmakeOptions[:]:
            if word.startswith('-DCMAKE_BUILD_TYPE'):
                cmakeOptions.remove(word)
            if word.startswith('-DCMAKE_CXX_FLAGS'):
                cmakeOptions.remove(word)
            if word.startswith('-DCMAKE_C_FLAGS'):
                cmakeOptions.remove(word)
        BuildTypeOptions.extend([
                 '-DCMAKE_BUILD_TYPE=None',
                 '-DCMAKE_CXX_FLAGS=%s'         % compile_flags,
                 '-DCMAKE_C_FLAGS=%s'           % compile_flags
        ])

        cmakeOptions.extend(BuildTypeOptions)

    def set_mpi_cmakeOptions(self, spec, cmakeOptions):
        # Appends to cmakeOptions the options that will enable the appropriate MPI implementations
 
        MPIOptions = []

        # openmpi
        if '+openmpi' in spec:
            MPIOptions.extend([
                 '-DOPENMPI_DIR=%s' % spec['openmpi'].prefix
            ])
        # mpich
        if '+mpich' in spec:
            MPIOptions.extend([
                 '-DMPICH_DIR=%s' % spec['mpich'].prefix
            ])
        # mpich2
        if '+mpich2' in spec:
            MPIOptions.extend([
                 '-DMPICH2_DIR=%s' % spec['mpich2'].prefix
            ])
        # mvapich
        if '+mvapich' in spec:
            MPIOptions.extend([
                 '-DMVAPICH_DIR=%s' % spec['mvapich'].prefix
            ])
        # mvapich2
        if '+mvapich2' in spec:
            MPIOptions.extend([
                 '-DMVAPICH2_DIR=%s' % spec['mvapich2'].prefix
            ])
        # mpt
        if '+mpt' in spec:
            MPIOptions.extend([
                 '-DMPT_DIR=%s' % spec['mpt'].prefix
            ])

        cmakeOptions.extend(MPIOptions)

    def setup_environment(self, spack_env, run_env):
        """Set up the compile and runtime environments for a package."""

        # Common settings to both offline and cbtf versions of OpenSpeedShop
        run_env.prepend_path('PATH', self.prefix.bin)

        # sqlite3 path
        run_env.prepend_path('PATH', self.spec['sqlite'].prefix.bin)

        # python path
        run_env.prepend_path('PATH', self.spec['python'].prefix.bin)

        # Find Dyninst library path
        dyninst_libdir = find_libraries(['libdyninstAPI_RT'], root=self.spec['dyninst'].prefix, shared=True, recurse=True)
        
        # Set Dyninst RT library path to support OSS loop resolution code
        run_env.set('DYNINSTAPI_RT_LIB', dyninst_libdir)

        # Find openspeedshop library path
        oss_libdir = find_libraries(['libopenss-framework'], root=self.spec['openspeedshop'].prefix, shared=True, recurse=True)
        run_env.prepend_path('LD_LIBRARY_PATH', os.path.dirname(oss_libdir.joined()))

        # This is always python lib everywhere we have seen to date.
        run_env.prepend_path('LD_LIBRARY_PATH', self.spec['python'].prefix.lib)

        # This is always boost lib everywhere we have seen to date.
        run_env.prepend_path('LD_LIBRARY_PATH', self.spec['boost'].prefix.lib)

        # Find sqlite library path
        sqlite_libdir = find_libraries(['libsqlite3'], root=self.spec['sqlite'].prefix, shared=True, recurse=True)
        run_env.prepend_path('LD_LIBRARY_PATH', os.path.dirname(sqlite_libdir.joined()))

        # see above for dyninst_libdir detection code
        run_env.prepend_path('LD_LIBRARY_PATH', os.path.dirname(dyninst_libdir.joined()))

        # Find libelf library path
        libelf_libdir = find_libraries(['libelf'], root=self.spec['libelf'].prefix, shared=True, recurse=True)
        run_env.prepend_path('LD_LIBRARY_PATH', os.path.dirname(libelf_libdir.joined()))

        # Find libdwarf library path
        libdwarf_libdir = find_libraries(['libdwarf'], root=self.spec['libdwarf'].prefix, shared=True, recurse=True)
        run_env.prepend_path('LD_LIBRARY_PATH', os.path.dirname(libdwarf_libdir.joined()))

        # Settings specific to the version, checking here for the cbtf instrumentor
        if '+cbtf' in self.spec:
            run_env.set('XPLAT_RSH', 'ssh')
            run_env.set('MRNET_COMM_PATH', join_path(self.spec['cbtf-krell'].prefix + '/sbin/cbtf_mrnet_commnode'))
            run_env.set('CBTF_MRNET_BACKEND_PATH', join_path(self.spec['cbtf-krell'].prefix + '/sbin/cbtf_libcbtf_mrnet_backend'))
            run_env.prepend_path('PATH', self.spec['mrnet'].prefix.bin)
            run_env.prepend_path('PATH', self.spec['cbtf-krell'].prefix.bin)
            run_env.prepend_path('PATH', self.spec['cbtf-krell'].prefix.sbin)

            # Find cbtf-krell component library path
            cbtfkrell_libdir = find_libraries(['libcbtf-core'], root=self.spec['cbtf-krell'].prefix, shared=True, recurse=True)
            run_env.prepend_path('LD_LIBRARY_PATH', os.path.dirname(cbtfkrell_libdir.joined()))

            # Find cbtf component library path
            cbtf_libdir = find_libraries(['libcbtf'], root=self.spec['cbtf'].prefix, shared=True, recurse=True)
            run_env.prepend_path('LD_LIBRARY_PATH', os.path.dirname(cbtf_libdir.joined()))

            # see above for dyninst_libdir detection code
            run_env.prepend_path('LD_LIBRARY_PATH', os.path.dirname(dyninst_libdir.joined()))

            # Find xercesc component library path
            xercesc_libdir = find_libraries(['libxerces-c'], root=self.spec['xerces-c'].prefix, shared=True, recurse=True)
            run_env.prepend_path('LD_LIBRARY_PATH', os.path.dirname(xercesc_libdir.joined()))

            # Find mrnet component library path
            mrnet_libdir = find_libraries(['libmrnet'], root=self.spec['mrnet'].prefix, shared=True, recurse=True)
            run_env.prepend_path('LD_LIBRARY_PATH', os.path.dirname(mrnet_libdir.joined()))

        elif '+offline' in self.spec:
            # Had to use this form of syntax self.prefix.lib and self.prefix.lib64 returned None all the time
            run_env.set('OPENSS_RAWDATA_DIR', '.')
            run_env.set('OPENSS_PLUGIN_PATH', join_path(oss_libdir + '/openspeedshop'))
            run_env.prepend_path('PATH', self.spec['papi'].prefix.bin)
            run_env.prepend_path('PATH', self.spec['libdwarf'].prefix.bin)

            # Find papi library path
            papi_libdir = find_libraries(['libpapi'], root=self.spec['papi'].prefix, shared=True, recurse=True)
            run_env.prepend_path('LD_LIBRARY_PATH', os.path.dirname(papi_libdir.joined()))

            # Find binutils library path
            binutils_libdir = find_libraries(['libbfd'], root=self.spec['binutils'].prefix, shared=True, recurse=True)
            run_env.prepend_path('LD_LIBRARY_PATH', os.path.dirname(binutils_libdir.joined()))

            # Find libmonitor library path
            libmonitor_libdir = find_libraries(['libmonitor'], root=self.spec['monitor'].prefix, shared=True, recurse=True)
            run_env.prepend_path('LD_LIBRARY_PATH', os.path.dirname(libmonitor_libdir.joined()))

            # Find libunwind library path
            libunwind_libdir = find_libraries(['libunwind'], root=self.spec['libunwind'].prefix, shared=True, recurse=True)
            run_env.prepend_path('LD_LIBRARY_PATH', os.path.dirname(libunwind_libdir.joined()))

            if '+mpich' in self.spec:
                run_env.set('OPENSS_MPI_IMPLEMENTATION', 'mpich')
            if '+mpich2' in self.spec:
                run_env.set('OPENSS_MPI_IMPLEMENTATION', 'mpich2')
            if '+mvapich2' in self.spec:
                run_env.set('OPENSS_MPI_IMPLEMENTATION', 'mvapich2')
            if '+openmpi' in self.spec:
                run_env.set('OPENSS_MPI_IMPLEMENTATION', 'openmpi')

    def install(self, spec, prefix):

        if '+offline' in spec:
            instrumentor_setting = "offline"
            if '+runtime' in spec:
                with working_dir('build_runtime', create=True):

                    cmakeOptions = []
                    cmakeOptions.extend(['-DCMAKE_INSTALL_PREFIX=%s'   % prefix,
                                         '-DINSTRUMENTOR=%s'           % instrumentor_setting,
                                         '-DLIBMONITOR_DIR=%s'         % spec['libmonitor'].prefix,
                                         '-DLIBUNWIND_DIR=%s'          % spec['libunwind'].prefix,
                                         '-DPAPI_DIR=%s'               % spec['papi'].prefix 
                                        ])
 
                    # Add any MPI implementations coming from variant settings
                    self.set_mpi_cmakeOptions(spec, cmakeOptions)
                    cmakeOptions.extend(std_cmake_args)

                    # Adjust the build options to the favored ones for this build
                    self.adjustBuildTypeParams_cmakeOptions(spec, cmakeOptions)

                    cmake('..', *cmakeOptions)

                    make("clean")
                    make()
                    make("install")
            else:
                cmake_prefix_path = join_path(spec['dyninst'].prefix)
                with working_dir('build', create=True):

                    python_vers=format(spec['python'].version.up_to(2))

                    cmakeOptions = []
                    cmakeOptions.extend(['-DCMAKE_INSTALL_PREFIX=%s'   % prefix,
                                         '-DCMAKE_PREFIX_PATH=%s'      % cmake_prefix_path,
                                         '-DINSTRUMENTOR=%s'           % instrumentor_setting,
                                         '-DBINUTILS_DIR=%s'           % spec['binutils'].prefix,
                                         '-DLIBELF_DIR=%s'             % spec['libelf'].prefix,
                                         '-DLIBDWARF_DIR=%s'           % spec['libdwarf'].prefix,
                                         '-DLIBMONITOR_DIR=%s'         % spec['libmonitor'].prefix,
                                         '-DLIBUNWIND_DIR=%s'          % spec['libunwind'].prefix,
                                         '-DPAPI_DIR=%s'               % spec['papi'].prefix,
                                         '-DSQLITE3_DIR=%s'            % spec['sqlite'].prefix,
                                         '-DQTLIB_DIR=%s'              % spec['qt'].prefix,
                                         '-DPYTHON_EXECUTABLE=%s'      % join_path(spec['python'].prefix + '/bin/python'),
                                         '-DPYTHON_INCLUDE_DIR=%s'     % join_path(spec['python'].prefix.include) + '/python' + python_vers,
                                         '-DPYTHON_LIBRARY=%s'         % join_path(spec['python'].prefix.lib) + '/libpython' + python_vers + '.so',
                                         '-DBoost_NO_SYSTEM_PATHS=TRUE',
                                         '-DBoost_NO_BOOST_CMAKE=TRUE',
                                         '-DBOOST_ROOT=%s'             % spec['boost'].prefix,
                                         '-DBoost_DIR=%s'              % spec['boost'].prefix,
                                         '-DBOOST_LIBRARYDIR=%s'       % spec['boost'].prefix.lib,
                                         '-DDYNINST_DIR=%s'            % spec['dyninst'].prefix
                                        ])

                    # Add any MPI implementations coming from variant settings
                    self.set_mpi_cmakeOptions(spec, cmakeOptions)
                    cmakeOptions.extend(std_cmake_args)

                    # Adjust the build options to the favored ones for this build
                    self.adjustBuildTypeParams_cmakeOptions(spec, cmakeOptions)

                    cmake('..', *cmakeOptions)

                    make("clean")
                    make()
                    make("install")

        elif '+cbtf' in spec:
            instrumentor_setting = "cbtf"
            resolve_symbols = "symtabapi"
            cmake_prefix_path = join_path(spec['cbtf'].prefix) + ':' + join_path(spec['cbtf-krell'].prefix) + ':' + join_path(spec['dyninst'].prefix)
            #runtime_platform_cray = "cray"
            #if '+cray' in spec:
            #    if '+runtime' in spec:
            #                   #-DCBTF_KRELL_CN_RUNTIME_DIR=${CBTF_KRELL_CN_INSTALL_DIR} \
            #        with working_dir('build_cbtf_cray_runtime', create=True):
            #            python_vers='%d.%d' % spec['python'].version[:2]
            #            cmake('..',
            #                  '-DCMAKE_INSTALL_PREFIX=%s'   % prefix,
            #                  '-DRUNTIME_PLATFORM=%s'		% runtime_platform_cray,
            #                  '-DCMAKE_PREFIX_PATH=%s'      % cmake_prefix_path,
            #                  '-DRESOLVE_SYMBOLS=%s'		% resolve_symbols,
            #                  '-DINSTRUMENTOR=%s'           % instrumentor_setting,
            #                  '-DCBTF_DIR=%s'			% spec['cbtf'].prefix,
            #                  '-DCBTF_KRELL_DIR=%s'		% spec['cbtf-krell'].prefix,
            #                  '-DCBTF_KRELL_CN_RUNTIME_DIR=%s'	% spec['cbtf-krell'].prefix,
            #                  '-DBINUTILS_DIR=%s'           % spec['binutils'].prefix,
            #                  '-DLIBELF_DIR=%s'             % spec['libelf'].prefix,
            #                  '-DLIBDWARF_DIR=%s'           % spec['libdwarf'].prefix,
            #                  '-DLIBUNWIND_DIR=%s'          % spec['libunwind'].prefix,
            #                  '-DPAPI_DIR=%s'               % spec['papi'].prefix,
            #                  '-DDYNINST_DIR=%s'            % spec['dyninst'].prefix,
            #                  '-DXERCESC_DIR=%s'            % spec['xerces-c'].prefix,
            #                  '-DMRNET_DIR=%s'              % spec['mrnet'].prefix,
            #                  '-DBoost_NO_SYSTEM_PATHS=TRUE',
            #                  '-DBOOST_ROOT=%s'             % spec['boost'].prefix,
            #                  *std_cmake_args)

            #           make("clean")
            #           make()
            #           make("install")


            #elif '+mic' in spec:
            # comment out else and shift over the default case below until arch detection is in
            #else:

            if '+runtime' in spec:
                with working_dir('build_cbtf_runtime', create=True):
                    python_vers='%d.%d' % spec['python'].version[:2]
                    cmakeOptions = []
                    cmakeOptions.extend(['-DCMAKE_INSTALL_PREFIX=%s'   % prefix,
                          '-DCMAKE_PREFIX_PATH=%s'      % cmake_prefix_path,
                          '-DINSTRUMENTOR=%s'           % instrumentor_setting,
                          '-DBINUTILS_DIR=%s'           % spec['binutils'].prefix,
                          '-DLIBELF_DIR=%s'             % spec['libelf'].prefix,
                          '-DLIBDWARF_DIR=%s'           % spec['libdwarf'].prefix,
                          '-DCBTF_DIR=%s'               % spec['cbtf'].prefix,
                          '-DCBTF_KRELL_DIR=%s'         % spec['cbtf-krell'].prefix,
                          '-DPYTHON_EXECUTABLE=%s'      % join_path(spec['python'].prefix + '/bin/python'),
                          '-DPYTHON_INCLUDE_DIR=%s'     % join_path(spec['python'].prefix.include) + '/python' + python_vers,
                          '-DPYTHON_LIBRARY=%s'         % join_path(spec['python'].prefix.lib) + '/libpython' + python_vers + '.so',
                          '-DBoost_NO_SYSTEM_PATHS=TRUE',
                          '-DBoost_NO_BOOST_CMAKE=TRUE',
                          '-DBOOST_ROOT=%s'             % spec['boost'].prefix,
                          '-DBoost_DIR=%s'              % spec['boost'].prefix,
                          '-DBOOST_LIBRARYDIR=%s'       % spec['boost'].prefix.lib,
                          '-DBoost_INCLUDE_DIRS:PATH=%s' % spec['boost'].prefix.include,
                          '-DBoost_LIBRARY_DIRS:PATH=%s' % spec['boost'].prefix.lib,
                          '-DDYNINST_DIR=%s'            % spec['dyninst'].prefix,
                          '-DMRNET_DIR=%s'              % spec['mrnet'].prefix
                          ])

                    # Add any MPI implementations coming from variant settings
                    #self.set_mpi_cmakeOptions(spec, cmakeOptions)
                    #cmakeOptions.extend(std_cmake_args)

                    # Adjust the build options to the favored ones for this build
                    self.adjustBuildTypeParams_cmakeOptions(spec, cmakeOptions)

                    cmake('..', *cmakeOptions)

                    make("clean")
                    make()
                    make("install")

            else:
                with working_dir('build_cbtf', create=True):
                    python_vers=format(spec['python'].version.up_to(2))
                    cmakeOptions = []
                    cmakeOptions.extend(['-DCMAKE_INSTALL_PREFIX=%s'   % prefix,
                          '-DCMAKE_PREFIX_PATH=%s'      % cmake_prefix_path,
                          '-DINSTRUMENTOR=%s'           % instrumentor_setting,
                          '-DBINUTILS_DIR=%s'           % spec['binutils'].prefix,
                          '-DLIBELF_DIR=%s'             % spec['libelf'].prefix,
                          '-DLIBDWARF_DIR=%s'           % spec['libdwarf'].prefix,
                          '-DSQLITE3_DIR=%s'            % spec['sqlite'].prefix,
                          '-DCBTF_DIR=%s'               % spec['cbtf'].prefix,
                          '-DCBTF_KRELL_DIR=%s'         % spec['cbtf-krell'].prefix,
                          '-DQTLIB_DIR=%s'              % spec['qt'].prefix,
                          '-DPYTHON_EXECUTABLE=%s'      % join_path(spec['python'].prefix + '/bin/python'),
                          '-DPYTHON_INCLUDE_DIR=%s'     % join_path(spec['python'].prefix.include) + '/python' + python_vers,
                          '-DPYTHON_LIBRARY=%s'         % join_path(spec['python'].prefix.lib) + '/libpython' + python_vers + '.so',
                          '-DBoost_NO_SYSTEM_PATHS=TRUE',
                          '-DBoost_NO_BOOST_CMAKE=TRUE',
                          '-DBOOST_ROOT=%s'             % spec['boost'].prefix,
                          '-DBoost_DIR=%s'              % spec['boost'].prefix,
                          '-DBOOST_LIBRARYDIR=%s'       % spec['boost'].prefix.lib,
                          '-DBoost_INCLUDE_DIRS:PATH=%s' % spec['boost'].prefix.include,
                          '-DBoost_LIBRARY_DIRS:PATH=%s' % spec['boost'].prefix.lib,
                          '-DDYNINST_DIR=%s'            % spec['dyninst'].prefix,
                          '-DMRNET_DIR=%s'              % spec['mrnet'].prefix
                          ])

                    # Add any MPI implementations coming from variant settings
                    #self.set_mpi_cmakeOptions(spec, cmakeOptions)
                    #cmakeOptions.extend(std_cmake_args)

                    # Adjust the build options to the favored ones for this build
                    self.adjustBuildTypeParams_cmakeOptions(spec, cmakeOptions)

                    cmake('..', *cmakeOptions)

                    make("clean")
                    make()
                    make("install")

        #if '+frontend' in spec:
        #    with working_dir('build_frontend', create=True):
        #         tbd



        #if '+cbtf' in spec:
        #   if cray build type detected:
        #        if '+runtime' in spec:
        #            with working_dir('build_cray_cbtf_compute', create=True):
        #                tbd
        #        else:
        #            with working_dir('build_cray_cbtf_frontend', create=True):
        #                tbd
        #            with working_dir('build_cray_osscbtf_frontend', create=True):
        #                tbd
        #        fi
        #    elif '+intelmic' in spec:
        #        if '+runtime' in spec:
        #            with working_dir('build_intelmic_cbtf_compute', create=True):
        #                tbd
        #        else:
        #            with working_dir('build_intelmic_cbtf_frontend', create=True):
        #                tbd
        #            with working_dir('build_intelmic_osscbtf_frontend', create=True):
        #        fi
        #    else
        #        with working_dir('build_cluster_cbtf', create=True):
        #             tbd
        #        with working_dir('build_cluster osscbtf', create=True):
        #             tbd
        #    fi
        #elif '+offline' in spec:
        #   if cray build type detected:
        #        if '+runtime' in spec:
        #            with working_dir('build_cray_ossoff_compute', create=True):
        #                tbd
        #        else:
        #            with working_dir('build_cray_ossoff_frontend', create=True):
        #                tbd
        #        fi
        #    elif '+intelmic' in spec:
        #        if '+runtime' in spec:
        #            with working_dir('build_intelmic_ossoff_compute', create=True):
        #                tbd
        #        else:
        #            with working_dir('build_intelmic_ossoff_frontend', create=True):
        #                tbd
        #        fi
        #    elif bgq build type detected:
        #        if '+runtime' in spec:
        #            with working_dir('build_bgq_ossoff_compute', create=True):
        #                tbd
        #        else:
        #            with working_dir('build_bgq_ossoff_frontend', create=True):
        #                tbd
        #        fi
        #    else
        #        with working_dir('build_cluster ossoff', create=True):
        #             tbd
        #    fi
        #fi


