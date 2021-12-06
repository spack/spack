# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyGosam(PythonPackage):
    """The package GoSam allows for the automated calculation of
       one-loop amplitudes for multi-particle processes in renormalizable
       quantum field theories."""

    homepage = "https://github.com/gudrunhe/gosam"
    git      = "https://github.com/gudrunhe/gosam.git"

    tags = ['hep']

    version('2.1.1', tag='2.1.1', commit='4b98559212dfcb71f9d983a3a605e4693ac7f83f')
    version('2.0.4', sha256='faf621c70f66d9dffc16ac5cce66258067f39f686d722a4867eeb759fcde4f44',
            url='https://gosam.hepforge.org/downloads/?f=gosam-2.0.4-6d9f1cba.tar.gz')
    version('2.0.3', tag='v2.0.3', commit='4146ab23a06b7c57c10fb36df60758d34aa58387')

    depends_on('form', type='run')
    depends_on('qgraf', type='run')
    depends_on('gosam-contrib', type='link')
    depends_on('python@2.7.0:2.7', type=('build', 'run'), when='@:2.0.4')
    depends_on('python@3:', type=('build', 'run'), when='@2.1.1:')

    def setup_run_environment(self, env):
        gosam_contrib_lib_dir = self.spec['gosam-contrib'].prefix.lib
        env.prepend_path('LD_LIBRARY_PATH', gosam_contrib_lib_dir)
