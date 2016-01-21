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

class CbtfKrell(Package):
    """CBTF Krell project contains the Krell Institute contributions to the CBTF project. 
       These contributions include many performance data collectors and support 
       libraries as well as some example tools that drive the data collection at 
       HPC levels of scale."""
    homepage = "http://sourceforge.net/p/cbtf/wiki/Home/"

    # optional mirror access template
    #url      = "file:/g/g24/jeg/cbtf-krell-1.5.tar.gz"
    #version('1.5', 'b13f6df6a93c44149d977773dd776d2f')

    version('1.6', branch='master', git='http://git.code.sf.net/p/cbtf-krell/cbtf-krell')


    # Dependencies for cbtf-krell

    # For binutils service
    depends_on("binutils@2.24+krellpatch")

    # collectionTool
    depends_on("boost@1.50.0")
    depends_on("dyninst@8.2.1")
    depends_on("mrnet@4.1.0:+lwthreads")
    depends_on("xerces-c@3.1.1:")
    depends_on("cbtf")

    # for services and collectors
    depends_on("libmonitor+krellpatch")
    depends_on("libunwind")
    depends_on("papi")

    # MPI Installations
    # These have not worked either for build or execution, commenting out for now
    #depends_on("openmpi")
    #depends_on("mvapich2@2.0")
    #depends_on("mpich")

    parallel = False

    def install(self, spec, prefix):

        # Add in paths for finding package config files that tell us where to find these packages
        cmake_prefix_path = join_path(spec['cbtf'].prefix) + ':' + join_path(spec['dyninst'].prefix)

        # FIXME - hard code path until external package support is available
        # Need to change this path and/or add additional paths for MPI experiment support on different platforms
        #openmpi_prefix_path = "/opt/openmpi-1.8.2"
        #mvapich_prefix_path = "/usr/local/tools/mvapich-gnu"

        # Other possibilities, they will need a -DMVAPICH_DIR=, etc clause in the cmake command to be recognized
        # mvapich_prefix_path = "<mvapich install path>"
        # mvapich2_prefix_path = "<mvapich2 install path>"
        # mpich2_prefix_path = "<mpich2 install path>"
        # mpich_prefix_path = "<mpich install path>"
        # mpt_prefix_path = "<mpt install path>"

        # Add in paths for cuda if requested via the cuda variant
        # FIXME - hard code path until external package support is available
        #if '+cuda' in spec:
        #    cuda_prefix_path = "/usr/local/cuda-6.0"
        #    cupti_prefix_path = "/usr/local/cuda-6.0/extras/CUPTI"
        #else:
        #    cuda_prefix_path = ""
        #    cupti_prefix_path = ""

        #'-DMVAPICH2_DIR=%s'           % spec['mvapich2'].prefix,
        #'-DOPENMPI_DIR=%s'            % spec['openmpi'].prefix,
        #'-DMPICH_DIR=%s'              % spec['mpich'].prefix,
        #'-DCMAKE_LIBRARY_PATH=%s'	% prefix.lib64,
        #'-DOPENMPI_DIR=%s'            % openmpi_prefix_path,
        #'-DMVAPICH_DIR=%s'            % mvapich_prefix_path,
        #'-DLIB_SUFFIX=64',
        #'-DCUDA_DIR=%s'               % cuda_prefix_path,
        #'-DCUPTI_DIR=%s'              % cupti_prefix_path,

        # Build cbtf-krell with cmake 
        with working_dir('build_cbtf_krell', create=True):
            cmake('..',
                  '-DCMAKE_BUILD_TYPE=Debug',
                  '-DCMAKE_INSTALL_PREFIX=%s'	% prefix,
                  '-DCBTF_DIR=%s'		% spec['cbtf'].prefix,
                  '-DBINUTILS_DIR=%s'           % spec['binutils'].prefix,
                  '-DLIBMONITOR_DIR=%s'         % spec['libmonitor'].prefix,
                  '-DLIBUNWIND_DIR=%s'          % spec['libunwind'].prefix,
                  '-DPAPI_DIR=%s'               % spec['papi'].prefix,
                  '-DBOOST_DIR=%s'              % spec['boost'].prefix,
                  '-DMRNET_DIR=%s'              % spec['mrnet'].prefix,
                  '-DDYNINST_DIR=%s'		% spec['dyninst'].prefix,
                  '-DXERCESC_DIR=%s'            % spec['xerces-c'].prefix,
                  '-DCMAKE_PREFIX_PATH=%s'	% cmake_prefix_path,
                  *std_cmake_args)

            make("clean")
            make()
            make("install")

