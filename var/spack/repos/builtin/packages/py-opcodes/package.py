# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.pkgkit import *


class PyOpcodes(PythonPackage):
    """Database of Processor Instructions/Opcodes."""

    homepage = "https://github.com/Maratyszcza/Opcodes"
    pypi     = "opcodes/opcodes-0.3.14.tar.gz"

    version('0.3.14', sha256='16ec1cea4cf3dda767e6c0a718f664ef97a34ed24c91998a3c25c3f960c15fba')

    depends_on('py-setuptools', type=('build', 'run'))
