# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class ConnectomeTools(PythonPackage):
    """Connectome statistics; S2F recipe generation"""

    homepage = "https://bbpcode.epfl.ch/code/#/admin/projects/nse/connectome-tools"
    git      = "ssh://bbpcode.epfl.ch/nse/connectome-tools"

    version('develop', branch='master')
    version('0.3.0', tag='connectome-tools-v0.3.0', preferred=True)

    depends_on('py-setuptools', type=('build', 'run'))

    depends_on('py-click@7.0:7.999', type='run')
    depends_on('py-equation@1.2:', type='run')
    depends_on('py-lxml@3.3:', type='run')
    depends_on('py-numpy@1.9:', type='run')
    depends_on('py-pandas@0.17:', type='run')
    depends_on('py-six@1.0:', type='run')

    depends_on('py-bluepy@0.13.3:', type='run')
    depends_on('py-voxcell@2.5.6:', type='run')
