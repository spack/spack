################################################################################
# Copyright (c) 2015 Krell Institute. All Rights Reserved.
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
    url      = "http://sourceforge.net/projects/openss/files/openss/openspeedshop-2.2/openspeedshop-2.2.tar.gz/download"
    version('2.2', '16cb051179c2038de4e8a845edf1d573')

    #homepage = "http://www.openspeedshop.org"
    #url      = "http://sourceforge.net/projects/openss/files/openss/openspeedshop-2.1/openspeedshop-2.1.tar.gz/download"
    #version('2.1', 'bdaa57c1a0db9d0c3e0303fd8496c507')

    # optional mirror template
    #url      = "file:/g/g24/jeg/openspeedshop-2.1.tar.gz"
    #version('2.1', '64ee17166519838c7b94a1adc138e94f')



    parallel = False

    variant('offline', default=True, description="build with offline instrumentor enabled.")
    variant('cbtf', default=False, description="build with cbtf instrumentor enabled.")
    variant('runtime', default=False, description="build only the runtime libraries and collectors.")
    variant('frontend', default=False, description="build only the front-end tool using the runtime_dir to point to the target build.")
    variant('cuda', default=False, description="build with cuda packages included.")
    variant('ptgf', default=False, description="build with the PTGF based gui package enabled.")
    variant('intelmic', default=False, description="build for the Intel MIC platform.")
    variant('cray', default=False, description="build for Cray platforms.")
    variant('bluegene', default=False, description="build for Cray platforms.")
    variant('rtfe', default=False, description="build for generic cluster platforms that have different processors on the fe and be nodes.")

    # Dependencies for openspeedshop that are common to all the variants of the OpenSpeedShop build
    depends_on("bison")
    depends_on("flex")
    depends_on("binutils@2.24+krellpatch")
    depends_on("libelf")
    depends_on("libdwarf")
    depends_on("sqlite")
    depends_on("boost@1.50.0")
    depends_on("dyninst@8.2.1")
    depends_on("python")
    depends_on("qt@3.3.8b+krellpatch")

    # Dependencies only for the openspeedshop offline package.
    depends_on("libunwind", when='+offline')
    depends_on("papi", when='+offline')
    depends_on("libmonitor+krellpatch", when='+offline')
    #depends_on("openmpi+krelloptions", when='+offline')
    #depends_on("openmpi", when='+offline')
    #depends_on("mpich", when='+offline')

    # Dependencies only for the openspeedshop cbtf package.
    depends_on("cbtf", when='+cbtf')
    depends_on("cbtf-krell", when='+cbtf')
    depends_on("cbtf-argonavis", when='+cbtf')
    depends_on("mrnet@4.1.0:+lwthreads", when='+cbtf')

    def install(self, spec, prefix):

        #openmpi_prefix_path = "/opt/openmpi-1.8.2"
        #mvapich_prefix_path = "/usr/local/tools/mvapich-gnu"
                          #'-DOPENMPI_DIR=%s'            % spec['openmpi'].prefix,
                          #'-DOPENMPI_DIR=%s'            % openmpi_prefix_path,
                          #'-DMVAPICH_DIR=%s'            % mvapich_prefix_path,

        # FIXME: How do we make this dynamic in spack?   That is, can we specify the paths to cuda dynamically?
        # WAITING for external package support. 
        #if '+cuda' in spec:
        #    cuda_prefix_path = "/usr/local/cuda-6.0"
        #    cupti_prefix_path = "/usr/local/cuda-6.0/extras/CUPTI"

        if '+offline' in spec:
            instrumentor_setting = "offline"
            if '+runtime' in spec:
                with working_dir('build_runtime', create=True):
                    cmake('..',
                          '-DCMAKE_INSTALL_PREFIX=%s'   % prefix,
                          '-DCMAKE_LIBRARY_PATH=%s'     % prefix.lib64,
                          '-DINSTRUMENTOR=%s'           % instrumentor_setting,
                          '-DLIBMONITOR_DIR=%s'         % spec['libmonitor'].prefix,
                          '-DLIBUNWIND_DIR=%s'          % spec['libunwind'].prefix,
                          '-DPAPI_DIR=%s'               % spec['papi'].prefix,
                          *std_cmake_args)
                    make("clean")
                    make()
                    make("install")
            else:
                cmake_prefix_path = join_path(spec['dyninst'].prefix)
                with working_dir('build', create=True):
                    #python_vers=join_path(spec['python'].version[:2])
                    #'-DOPENMPI_DIR=%s'            % openmpi_prefix_path,
                    #'-DMVAPICH_DIR=%s'            % mvapich_prefix_path,
                    python_vers='%d.%d' % spec['python'].version[:2]
                    cmake('..',
                          '-DCMAKE_INSTALL_PREFIX=%s'   % prefix,
                          '-DCMAKE_LIBRARY_PATH=%s'     % prefix.lib64,
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
                          '-DBOOST_ROOT=%s'             % spec['boost'].prefix,
                          '-DDYNINST_DIR=%s'            % spec['dyninst'].prefix,
                          *std_cmake_args)
                    make("clean")
                    make()
                    make("install")

        elif '+cbtf' in spec:
            instrumentor_setting = "cbtf"
            cmake_prefix_path = join_path(spec['cbtf'].prefix) + ':' + join_path(spec['cbtf-krell'].prefix) + ':' + join_path(spec['dyninst'].prefix)
            if '+runtime' in spec:
                with working_dir('build_cbtf_runtime', create=True):
                    python_vers='%d.%d' % spec['python'].version[:2]
                    cmake('..',
                          '-DCMAKE_INSTALL_PREFIX=%s'   % prefix,
                          '-DCMAKE_LIBRARY_PATH=%s'     % prefix.lib64,
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
                          '-DBOOST_ROOT=%s'             % spec['boost'].prefix,
                          '-DDYNINST_DIR=%s'            % spec['dyninst'].prefix,
                          '-DMRNET_DIR=%s'              % spec['mrnet'].prefix,
                          *std_cmake_args)
                    make("clean")
                    make()
                    make("install")

            else:
                with working_dir('build_cbtf', create=True):
                    python_vers='%d.%d' % spec['python'].version[:2]
                    #python_vers=join_path(spec['python'].version[:2])
                    cmake('..',
                          '-DCMAKE_INSTALL_PREFIX=%s'   % prefix,
                          '-DCMAKE_LIBRARY_PATH=%s'     % prefix.lib64,
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
                          '-DBOOST_ROOT=%s'             % spec['boost'].prefix,
                          '-DDYNINST_DIR=%s'            % spec['dyninst'].prefix,
                          '-DMRNET_DIR=%s'              % spec['mrnet'].prefix,
                          *std_cmake_args)
                    make("clean")
                    make()
                    make("install")

        #if '+frontend' in spec:
        #    with working_dir('build_frontend', create=True):
        #         tbd


        #if '+intelmic' in spec:
        #    with working_dir('build_intelmic_compute', create=True):
        #         tbd
        #    with working_dir('build_intelmic_frontend', create=True):
        #         tbd

        #if '+cray' in spec:
        #    with working_dir('build_cray_compute', create=True):
        #         tbd
        #    with working_dir('build_cray_frontend', create=True):
        #         tbd
