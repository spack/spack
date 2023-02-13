# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class PyKosh(PythonPackage):
    """
    Kosh allows codes to store, query, share data via an easy-to-use Python API.
    Kosh lies on top of Sina and can use any database backend supported by Sina.
    In adition Kosh aims to make data access and sharing as simple as possible.
    """

    homepage = "https://github.com/LLNL/kosh"
    url = "https://github.com/LLNL/kosh/archive/refs/tags/v2.0.tar.gz"

    # notify when the package is updated.
    maintainers("doutriaux1")

    version("2.2", sha256="3c79c3b7e7b64018ec5987dd7148886a6c619a28cda6f84e61a57439c9f3d7a3")
    version("2.1", sha256="597ed5beb4c3c3675b4af15ee7bfb60a463d5bda2222cd927061737ed073d562")
    version("2.0", sha256="059e431e3d3219b53956cb464d9e10933ca141dc89662f55d9c633e35c8b3a1e")

    depends_on("py-setuptools", type="build")
    depends_on("py-llnl-sina@1.11:", type=("build", "run"))
    depends_on("py-networkx", type=("build", "run"))
    depends_on("py-numpy", type=("build", "run"))
