# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyPylint(PythonPackage):
    """array processing for numbers, strings, records, and objects."""

    homepage = "https://pypi.python.org/pypi/pylint"
    url      = "https://pypi.io/packages/source/p/pylint/pylint-1.6.5.tar.gz"

    version('2.3.0', sha256='ee80c7af4f127b2a480d83010c9f0e97beb8eaa652b78c2837d3ed30b12e1182')
    version('1.9.4', sha256='ee1e85575587c5b58ddafa25e1c1b01691ef172e139fc25585e5d3f02451da93')
    # version('1.7.2', sha256='ea6afb93a9ed810cf52ff3838eb3a15e2bf6a81b80de0eaede1ce442caa5ca69') # see dependencies
    version('1.6.5', sha256='a673984a8dd78e4a8b8cfdee5359a1309d833cf38405008f4a249994a8456719')
    version('1.4.3', sha256='1dce8c143a5aa15e0638887c2b395e2e823223c63ebaf8d5f432a99e44b29f60')
    version('1.4.1', sha256='3e383060edd432cbbd0e8bd686f5facfe918047ffe1bb401ab5897cb6ee0f030')

    extends('python', ignore=r'bin/pytest')
    depends_on('py-astroid', type=('build', 'run'))
    # note there is no working version of astroid for this
    depends_on('py-astroid@1.5.1:', type=('build', 'run'), when='@1.7:')
    depends_on('py-astroid@1.6:1.9', type=('build', 'run'), when='@1.9.4:')
    depends_on('py-six', type=('build', 'run'))
    depends_on('py-isort@4.2.5:', type=('build', 'run'))
    depends_on('py-mccabe', type=('build', 'run'))
    depends_on('py-editdistance', type=('build', 'run'), when='@:1.7')
    depends_on('py-setuptools@17.1:', type='build')
    # depends_on('py-setuptools-scm@1.15.0:', type='build')
    depends_on('py-configparser', when='^python@:2.8', type=('build', 'run'))
    depends_on('py-backports-functools-lru-cache', when='^python@:2.8', type=('build', 'run'))
    depends_on('py-singledispatch', when='^python@:3.3.99', type=('build', 'run'))
