# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack import *


class PyKosh(PythonPackage):
    """Kosh allows codes to store, query, share data via an easy-to-use Python API.
Kosh lies on top of Sina and as a result can use any database backend supported by Sina.
In adition Kosh aims to make data access and sharing as simple as possible.
"""

    homepage = "https://github.com/LLNL/kosh"
    git = "https://github.com/LLNL/kosh.git"

    # notify when the package is updated.
    maintainers = [
        'doutriaux1',
    ]
    version('2.0', tag="v2.0")

    depends_on('py-setuptools', type='build')
    depends_on("py-sina", type=("build", "run"))
    depends_on("py-networkx", type=("build", "run"))
    depends_on("py-numpy", type=("build", "run"))

