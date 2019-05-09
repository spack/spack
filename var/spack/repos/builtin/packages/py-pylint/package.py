# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyPylint(PythonPackage):
    """array processing for numbers, strings, records, and objects."""

    homepage = "https://pypi.python.org/pypi/pylint"
    url      = "https://pypi.io/packages/source/p/pylint/pylint-1.6.5.tar.gz"

    version('2.3.0', sha256='ee80c7af4f127b2a480d83010c9f0e97beb8eaa652b78c2837d3ed30b12e1182')
    # version('1.7.2', '27ee752cdcfacb05bf4940947e6b35c6') # see dependencies
    version('1.6.5', '31da2185bf59142479e4fa16d8a9e347')
    version('1.4.3', '5924c1c7ca5ca23647812f5971d0ea44')
    version('1.4.1', 'df7c679bdcce5019389038847e4de622')

    extends('python', ignore=r'bin/pytest')
    depends_on('py-astroid', type=('build', 'run'))
    # note there is no working version of astroid for this
    depends_on('py-astroid@1.5.1:', type=('build', 'run'), when='@1.7:')
    depends_on('py-six', type=('build', 'run'))
    depends_on('py-isort@4.2.5:')
    depends_on('py-mccabe')
    depends_on('py-editdistance')
    depends_on('py-setuptools@17.1:', type='build')
    # depends_on('py-setuptools-scm@1.15.0:', type='build')
    depends_on('py-configparser', when='^python@:2.8')
    depends_on('py-backports-functools-lru-cache', when='^python@:2.8')
    depends_on('py-singledispatch', when='^python@:3.3.99')
