# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyTns(PythonPackage):
    """Python library for neuron synthesis"""

    homepage = "https://bbpcode.epfl.ch/code/#/admin/projects/molecularsystems/TNS"
    git      = "ssh://bbpcode.epfl.ch/molecularsystems/TNS"

    version('develop', branch='master')
    version('1.0.7', tag='tns-v1.0.7', preferred=True)

    depends_on('py-setuptools', type='build')

    depends_on('py-enum34@1.0:', type='run', when='^python@:3.3.99')
    depends_on('py-matplotlib@1.3:', type='run')
    depends_on('py-morphio@2.0:', type='run')
    depends_on('py-neurom@1.4:', type='run')
    depends_on('py-numpy@1.8:', type='run')
    depends_on('py-scipy@0.13:', type='run')
    depends_on('py-tmd@2.0.3:', type='run')
