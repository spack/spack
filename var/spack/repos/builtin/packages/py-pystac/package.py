# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyPystac(PythonPackage):
    """Python library for working with Spatiotemporal Asset Catalog (STAC)."""

    homepage = "https://github.com/azavea/pystac.git"
    pypi = "pystac/pystac-0.5.4.tar.gz"

    version("1.4.0", sha256="6ec43e1c6bec50fbfbdede49c3ccb83ecd112072a938001b5c9c581fc2945e83")
    version("1.3.0", sha256="b0244641ef2a29a7b7929266b0d1eda2b0a0ef826dadb1aed93404a14e6e313b")
    version("1.2.0", sha256="8a60be2a30e1e28f8617a88f9f8fddc00c519be494a02ec111dc8fba62bf26e7")
    version("1.1.0", sha256="de42e1de5e8dc7a75b97feea0b660efdb5500ad8d7a892ff47fc9ed08c3bc2df")
    version("1.0.1", sha256="3927f2104cd2077638e046b9c258d5e6b442bfabf2d179cbefbf10f509efae85")
    version("0.5.4", sha256="9fc3359364685adf54e3bc78c87550a8bc8b0a927405419bd8e4bbd42a8efc79")

    depends_on("python@3.7:", when="@1:", type=("build", "run"))
    depends_on("py-setuptools", type="build")
    depends_on("py-python-dateutil@2.7:", type=("build", "run"))
    depends_on("py-typing-extensions@3.7:", when="@1: ^python@:3.7", type=("build", "run"))
