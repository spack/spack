# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyConfigparser(PythonPackage):
    """This library brings the updated configparser from Python 3.5 to
    Python 2.6-3.5."""

    homepage = "https://docs.python.org/3/library/configparser.html"
    url      = "https://pypi.io/packages/source/c/configparser/configparser-3.5.0.tar.gz"

    version('3.5.0', 'cfdd915a5b7a6c09917a64a573140538')

    depends_on('py-setuptools', type='build')

    # This dependency breaks concretization
    # See https://github.com/spack/spack/issues/2793
    # depends_on('py-ordereddict', when='^python@:2.6', type=('build', 'run'))
