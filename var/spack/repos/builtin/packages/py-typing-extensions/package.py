# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyTypingExtensions(PythonPackage):
    """The typing_extensions module contains both backports of these
       changes as well as experimental types that will eventually be
       added to the typing module, such as Protocol (see PEP 544 for
       details about protocols and static duck typing)."""

    homepage = "https://github.com/python/typing/tree/master/typing_extensions"
    url      = "https://pypi.io/packages/source/t/typing_extensions/typing_extensions-3.7.2.tar.gz"

    version('3.7.2', sha256='fb2cd053238d33a8ec939190f30cfd736c00653a85a2919415cecf7dc3d9da71')

    depends_on('py-setuptools', type='build')
    depends_on('py-typing@3.6.4:', type=('build', 'run'))
