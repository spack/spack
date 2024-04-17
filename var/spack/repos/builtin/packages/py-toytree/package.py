# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyToytree(PythonPackage):
    """A minimalist tree manipulation and plotting library for use inside
    jupyter notebooks. Toytree combines a popular tree data structure
    based on the ete3 library with modern plotting tools based on the
    toyplot plotting library.
    """

    homepage = "https://github.com/eaton-lab/toytree"
    pypi = "toytree/toytree-2.0.1.tar.gz"

    maintainers("snehring")

    version(
        "2.0.1",
        sha256="300aa922ade2c642e6c78c1434d8c2566d1d23e410b5e81da8f5c87a62bc26da",
        url="https://pypi.org/packages/79/f8/1b3ff2d2801cb6bf74274b90325ff6a8145cedda99f0628d0d44f0489b47/toytree-2.0.1-py3-none-any.whl",
    )

    with default_args(type=("build", "run")):
        depends_on("py-future")
        depends_on("py-numpy", when="@1.2:")
        depends_on("py-requests")
        depends_on("py-toyplot", when="@1.2:")
