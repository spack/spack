# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyBrian2(PythonPackage):
    """A clock-driven simulator for spiking neural networks"""

    homepage = "http://www.briansimulator.org"
    url      = "https://pypi.io/packages/source/B/Brian2/Brian2-2.0.1.tar.gz"

    version('2.0.1', 'df5990e9a71f7344887bc02f54dfd0f0')
    version('2.0rc3', '3100c5e4eb9eb83a06ff0413a7d43152')

    variant('doc', default=False, description='Build the documentation')

    # depends on py-setuptools@6: for windows, if spack targets windows,
    # this will need to be added here
    depends_on('py-setuptools',     type='build')
    depends_on('py-numpy@1.8.2:',   type=('build', 'run'))
    depends_on('py-sympy@0.7.6:',   type=('build', 'run'))
    depends_on('py-pyparsing',      type=('build', 'run'))
    depends_on('py-jinja2@2.7:',    type=('build', 'run'))
    depends_on('py-cpuinfo@0.1.6:', type=('build', 'run'))
    depends_on('py-sphinx@1.4.2:',  type=('build', 'run'), when='+docs')
    depends_on('py-nosetests@1.0:', type='test')