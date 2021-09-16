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
    url      = "https://github.com/gudrunhe/gosam/archive/refs/tags/2.1.1.tar.gz"

    tags = ['hep']

    version('2.1.1', sha256='dd562675085123bef0c145fd5532c23eecd59f0176afc56fb5c832ca1b4233a6')
    version('2.0.4', sha256='faf621c70f66d9dffc16ac5cce66258067f39f686d722a4867eeb759fcde4f44',
            url='https://gosam.hepforge.org/downloads/?f=gosam-2.0.4-6d9f1cba.tar.gz')

    depends_on('form', type='run')
    depends_on('qgraf', type='run')
    depends_on('gosam-contrib', type='link')
    depends_on('python@2.7:2.7.99', type=('build', 'run'), when='@2.0.4')
    depends_on('python@3:', type=('build', 'run'), when='@2.1.1:')

    def setup_run_environment(self, env):
        gosam_contrib_lib_dir = self.spec['gosam-contrib'].prefix.lib
        env.prepend_path('LD_LIBRARY_PATH', gosam_contrib_lib_dir)
