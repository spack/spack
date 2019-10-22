# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyBrian2(PythonPackage):
    """A clock-driven simulator for spiking neural networks"""

    homepage = "http://www.briansimulator.org"
    url      = "https://pypi.io/packages/source/B/Brian2/Brian2-2.0.1.tar.gz"

    version('2.0.1', sha256='195d8ced0d20e9069917776948f92aa70b7457bbc6b5222b8199654402ee1153')
    version('2.0rc3', sha256='05f347f5fa6b25d1ce5ec152a2407bbce033599eb6664f32f5331946eb3c7d66')

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
