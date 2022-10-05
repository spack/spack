# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyHepdataLib(PythonPackage):
    """Library for getting your data into HEPData"""

    homepage = "https://github.com/HEPData/hepdata_lib"
    pypi = "hepdata_lib/hepdata_lib-0.9.0.tar.gz"

    version("0.10.1", sha256="f6c3b85975792d5fde14212a4f8212c507f9e961ba77271487a99518e89c8dd2")
    version("0.9.0", sha256="b7b194b8af0428f34094ac403f8794a672c82d85e33154161d6b3744cc2b9896")

    depends_on("py-setuptools", type="build")
    depends_on("root+python", type=("build", "run"))
    depends_on("py-numpy", type=("build", "run"))
    depends_on("py-pyyaml@4:", type=("build", "run"))
    depends_on("py-future", type=("build", "run"))
    depends_on("py-six", type=("build", "run"))
    depends_on("py-pytest-runner", type="build")
    depends_on("py-pytest-cov", type="build")
    depends_on("py-hepdata-validator@0.3.2:", when="@0.10.1:", type=("build", "run"))
