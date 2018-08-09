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
##########################################################################
# Copyright (c) 2015-2018 Krell Institute. All Rights Reserved.
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


class CbtfArgonavis(CMakePackage):
    """CBTF Argo Navis project contains the CUDA collector and supporting
       libraries that was done as a result of a DOE SBIR grant.
    """
    homepage = "http://sourceforge.net/p/cbtf/wiki/Home/"
    git      = "https://github.com/OpenSpeedShop/cbtf-argonavis.git"

    version('develop', branch='master')
    version('1.9.1.1', branch='1.9.1.1')
    version('1.9.1.0', branch='1.9.1.0')

    variant('cti', default=False,
            description="Build MRNet with the CTI startup option")
    variant('crayfe', default=False,
            description="build only the FE tool using the runtime_dir \
                         to point to target build.")
    variant('runtime', default=False,
            description="build only the runtime libraries and collectors.")
    variant('build_type', default='None', values=('None'),
            description='CMake build type')

    depends_on("cmake@3.0.2:", type='build')

    # To specify ^elfutils@0.170 on the command line spack
    # apparently needs/wants this dependency explicity here
    # even though it is referenced downstream
    depends_on("elf", type="link")

    # For boost
    depends_on("boost@1.50.0:", when='@develop')
    depends_on("boost@1.66.0", when='@1.9.1.0:9999')

    # For MRNet
    depends_on("mrnet@5.0.1-3:+cti", when='@develop+cti')
    depends_on("mrnet@5.0.1-3:+lwthreads", when='@develop~cti')
    depends_on("mrnet@5.0.1-3+cti", when='@1.9.1.0:9999+cti')
    depends_on("mrnet@5.0.1-3+lwthreads", when='@1.9.1.0:9999~cti')

    # For CBTF
    depends_on("cbtf@develop", when='@develop')
    depends_on("cbtf@1.9.1.0:9999", when='@1.9.1.0:9999')

    # For CBTF with cti
    depends_on("cbtf@develop+cti", when='@develop+cti')
    depends_on("cbtf@1.9.1.0:9999+cti", when='@1.9.1.0:9999+cti')

    # For CBTF with runtime
    depends_on("cbtf@develop+runtime", when='@develop+runtime')
    depends_on("cbtf@1.9.1.0:9999+runtime", when='@1.9.1.0:9999+runtime')

    # For libmonitor
    depends_on("libmonitor@2013.02.18+krellpatch")

    # For PAPI
    depends_on("papi", when='@develop')
    depends_on("papi@5.5.1", when='@1.9.1.0:9999')

    # For CBTF-KRELL
    depends_on("cbtf-krell@develop", when='@develop')
    depends_on("cbtf-krell@1.9.1.0:9999", when='@1.9.1.0:9999')

    depends_on('cbtf-krell@develop+cti', when='@develop+cti')
    depends_on('cbtf-krell@1.9.1.0:9999+cti', when='@1.9.1.0:9999+cti')

    depends_on('cbtf-krell@develop+runtime', when='@develop+runtime')
    depends_on('cbtf-krell@1.9.1.0:9999+runtime', when='@1.9.1.0:9999+runtime')

    # For CUDA
    depends_on("cuda")

    parallel = False

    build_directory = 'build_cbtf_argonavis'

    def cmake_args(self):
        spec = self.spec
        compile_flags = "-O2 -g"

        cmake_args = [
            '-DCMAKE_CXX_FLAGS=%s'         % compile_flags,
            '-DCMAKE_C_FLAGS=%s'           % compile_flags,
            '-DCUDA_DIR=%s' % spec['cuda'].prefix,
            '-DCUDA_INSTALL_PATH=%s' % spec['cuda'].prefix,
            '-DCUDA_TOOLKIT_ROOT_DIR=%s' % spec['cuda'].prefix,
            '-DCUPTI_DIR=%s' % spec['cuda'].prefix.extras.CUPTI,
            '-DCUPTI_ROOT=%s' % spec['cuda'].prefix.extras.CUPTI,
            '-DPAPI_ROOT=%s' % spec['papi'].prefix,
            '-DCBTF_DIR=%s' % spec['cbtf'].prefix,
            '-DCBTF_KRELL_DIR=%s' % spec['cbtf-krell'].prefix,
            '-DBOOST_ROOT=%s' % spec['boost'].prefix,
            '-DBoost_DIR=%s' % spec['boost'].prefix,
            '-DBOOST_LIBRARYDIR=%s' % spec['boost'].prefix.lib,
            '-DMRNET_DIR=%s' % spec['mrnet'].prefix,
            '-DLIBMONITOR_DIR=%s' % spec['libmonitor'].prefix,
            '-DBoost_NO_SYSTEM_PATHS=ON']

        return cmake_args

    def setup_environment(self, spack_env, run_env):
        """Set up the compile and runtime environments for a package."""

        run_env.prepend_path(
            'LD_LIBRARY_PATH',
            self.spec['cuda'].prefix + '/extras/CUPTI/lib64')
        spack_env.prepend_path(
            'LD_LIBRARY_PATH',
            self.spec['cuda'].prefix + '/extras/CUPTI/lib64')
