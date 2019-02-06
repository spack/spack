# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyPexpect(PythonPackage):
    """Pexpect allows easy control of interactive console applications."""
    homepage = "https://pypi.python.org/pypi/pexpect"
    url      = "https://pypi.io/packages/source/p/pexpect/pexpect-4.2.1.tar.gz"

    version('4.6.0', 'd4f3372965a996238d57d19b95d2e03a')
    version('4.2.1', '3694410001a99dff83f0b500a1ca1c95')
    version('3.3', '0de72541d3f1374b795472fed841dce8')

    depends_on('py-ptyprocess', type=('build', 'run'))
