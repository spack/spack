# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: MIT
#
# ----------------------------------------------------------------------------
#
#     spack install py-pypeg2
#
# You can edit this file again by typing:
#
#     spack edit py-pypeg2
#
# See the Spack documentation for more information on packaging.
# ----------------------------------------------------------------------------

from spack import *


class PyPypeg2(PythonPackage):
    """A PEG Parser-Interpreter in Python"""

    homepage = "https://fdik.org/pyPEG2/"
    url      = "https://files.pythonhosted.org/packages/f9/bd/10398e2c2d2070cc8a9c7153abfbd4ddb2895a2c52a32722ab8689e0cc7d/pyPEG2-2.15.2.tar.gz"

    version('2.15.2', '84057d292808553290f0b78f42c64bbe')

    depends_on('py-setuptools', type='build')
