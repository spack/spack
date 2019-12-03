# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyCmakeFormat(PythonPackage):
    """Source code formatter for cmake listfiles."""

    homepage = "https://github.com/cheshirekow/cmake_format"
    url      = "https://pypi.io/packages/source/c/cmake_format/cmake_format-0.4.5.tar.gz"

    version('0.6.0', sha256='fc9795907c508b4a1f851eba311bd7478b374a4ba4430cdda976ebbec440376a')
    version('0.4.5', sha256='16602408c774cd989ecfa25883de4c2dbac937e3890b735be4aab76f9647875a')

    depends_on('py-setuptools', type=('build', 'run'))
    depends_on('py-pyyaml', type='run')
