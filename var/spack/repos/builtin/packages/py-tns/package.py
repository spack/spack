# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyTns(PythonPackage):
    """Python library for neuron synthesis"""

    homepage = "https://bbpcode.epfl.ch/code/#/admin/projects/molecularsystems/TNS"
    git      = "ssh://bbpcode.epfl.ch/molecularsystems/TNS"

    version('develop', branch='master')
    version('space2', branch='space2')
    version('2.5.0', tag='TNS-v2.5.0')
    version('2.4.5', tag='TNS-v2.4.5')

    depends_on('py-setuptools', type='build')

    depends_on('py-matplotlib@1.3.1:', type='run')
    depends_on('py-morphio@3.0:3.999', type='run')
    depends_on('py-neurom@3:3.999', type='run', when='@2.5.0:')
    depends_on('py-neurom@2:2.99', type='run', when='@:2.4.99')
    depends_on('py-numpy@1.15.0:', type='run')
    depends_on('py-scipy@0.13.3:', type='run')
    depends_on('py-tmd@2.0.8:', type='run')
    depends_on('py-jsonschema@3.0.1:', type='run')
