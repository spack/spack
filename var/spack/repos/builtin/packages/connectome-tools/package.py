# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class ConnectomeTools(PythonPackage):
    """Connectome statistics; S2F recipe generation"""

    homepage = "https://bbpgitlab.epfl.ch/nse/connectome-tools"
    git = "git@bbpgitlab.epfl.ch:nse/connectome-tools.git"

    version('develop', branch='main')
    version('0.6.0', tag='connectome-tools-v0.6.0')

    depends_on('py-setuptools', type=('build', 'run'))

    depends_on('py-click@7.0:8.999', type='run')
    depends_on('py-equation@1.2:', type='run')
    depends_on('py-joblib@1.0.1:', type='run')
    depends_on('py-jsonschema@3.2.0:3.999', type='run')
    depends_on('py-lxml@3.3:', type='run')
    depends_on('py-numpy@1.9:', type='run')
    depends_on('py-pandas@1.0.0:', type='run')
    depends_on('py-psutil@5.7.2:', type='run')
    depends_on('py-pyyaml@5.3.1:', type='run')
    depends_on('py-submitit@1.3.3:', type='run')

    depends_on('py-bluepy@2.3.0:2.999', type='run')
    depends_on('py-morphio@3.0.1:3.999', type='run')
    depends_on('py-voxcell@3.0:3.999', type='run')
