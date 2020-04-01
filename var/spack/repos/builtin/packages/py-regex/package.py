# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyRegex(PythonPackage):
    """Alternative regular expression module, to replace re."""

    homepage = "https://pypi.python.org/pypi/regex/"
    url      = "https://pypi.io/packages/source/r/regex/regex-2017.07.11.tar.gz"

    version('2019.11.1', sha256='720e34a539a76a1fedcebe4397290604cc2bdf6f81eca44adb9fb2ea071c0c69')
    version('2017.07.11', sha256='dbda8bdc31a1c85445f1a1b29d04abda46e5c690f8f933a9cc3a85a358969616')

    depends_on('py-setuptools', type='build', when='@2017.07.11')
