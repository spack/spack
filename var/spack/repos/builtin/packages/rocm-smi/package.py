# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack import *
from os import popen


class RocmSmi(MakefilePackage):
    """This tool exposes functionality for clock and temperature
       management of your ROCm enabled system"""

    homepage = "https://github.com/RadeonOpenCompute/ROC-smi"
    url      = "https://github.com/RadeonOpenCompute/ROC-smi/archive/rocm-3.5.0.tar.gz"

    maintainers = ['srekolam', 'arjun-raj-kuppala']
    version('3.5.0', sha256='4f46e947c415a4ac12b9f6989f15a42afe32551706b4f48476fba3abf92e8e7c')

    variant('build_type', default='Release', values=("Release", "Debug"), description='CMake build type')

    phases = ['edit', 'build']

    @run_after('build')
    def post_build(self):
        popen('cp -R {0}/rocm_smi.py {1}'.format(self.build_directory, prefix))
        popen('ln -srf {0}/rocm_smi.py {1}/rocm-smi'.format(prefix, prefix))

        popen('mkdir -p {0}/smi-test/tests'.format(prefix))
        popen('cp -R {0}/tests/ {1}/smi-test/'.format(self.build_directory,
                                                      prefix))
        popen('cp -R {0}/test-rocm-smi.sh {1}/smi-test'.format(
              self.build_directory, prefix))
