# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyNodeenv(PythonPackage):
    """Node.js virtual environment builder"""

    homepage = "https://github.com/ekalinin/nodeenv"
    url      = "https://files.pythonhosted.org/packages/00/6e/ed417bd1ed417ab3feada52d0c89ab0ed87d150f91590badf84273e047c9/nodeenv-1.3.3.tar.gz"

    version('1.3.3', sha256='ad8259494cf1c9034539f6cced78a1da4840a4b157e23640bc4a0c0546b0cb7a')

    depends_on('py-setuptools', type='build')
