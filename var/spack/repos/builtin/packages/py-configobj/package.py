# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyConfigobj(PythonPackage):
    """Config file reading, writing and validation.
    """

    homepage = "https://github.com/DiffSK/configobj"
    url      = "https://pypi.io/packages/source/c/configobj/configobj-5.0.6.tar.gz"

    version('5.0.6', sha256='a2f5650770e1c87fb335af19a9b7eb73fc05ccf22144eb68db7d00cd2bcb0902')
