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
    version('0.4.0', tag='connectome-tools-v0.4.0', preferred=True)
    version('0.3.4', tag='connectome-tools-v0.3.4')

    depends_on('py-setuptools', type=('build', 'run'))

    depends_on('py-click@7.0:7.999', type='run')
    depends_on('py-equation@1.2:', type='run')
    depends_on('py-joblib@0.16.0:', type='run')
    depends_on('py-lxml@3.3:', type='run')
    depends_on('py-numpy@1.9:', type='run')
    depends_on('py-pandas@1.0.0:', type='run')
    depends_on('py-psutil@5.7.2:', type='run')
    depends_on('py-pyyaml@5.3.1:', type='run')

    depends_on('py-bluepy@2.0:2.999', when='@0.4.0:', type='run')
    depends_on('py-voxcell@3.0:3.999', when='@0.4.0:', type='run')

    depends_on('py-bluepy@0.13.3:1.999', when='@:0.3.4', type='run')
    depends_on('py-voxcell@2.5.6:2.999', when='@:0.3.4', type='run')
