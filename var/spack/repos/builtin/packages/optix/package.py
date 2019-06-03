# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *

class Optix(Package):
    """Nvidia OptiX is a ray tracing API."""
    homepage = "https://developer.nvidia.com/optix"
    version('5.0.1','a1be032f246654ec4e4978b8c30e7774', extension='sh', expand=False)
    url = "file:///gpfs/bbp.cscs.ch/project/proj3/development/deployment/optix.sh"
    phases = [ 'install']

    def install(self, spec, prefix):
        set_executable('./optix.sh')
        install = Executable('./optix.sh')
        install('--skip-license', '--prefix=%s' % prefix)
