# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class PyPiper(PythonPackage):
    """A lightweight python toolkit for gluing together restartable,
    robust shell pipelines.
    """

    homepage = "https://github.com/databio/pypiper"
    pypi = "piper/piper-0.12.3.tar.gz"

    license("BSD-2-Clause")

    version(
        "0.12.3",
        sha256="b7da6286fc883d129bd3456179946bbe8f2f9455b81032ffcc97410b8f4dd572",
        url="https://pypi.org/packages/a1/ca/c102d69056eb6d3d235e623e801aeda1de509a9cc504b976163def8887ab/piper-0.12.3-py3-none-any.whl",
    )

    with default_args(type=("build", "run")):
        depends_on("py-attmap@0.12.5:", when="@0.12.3:0.13")
        depends_on("py-logmuse@0.2.4:", when="@0.12.3:")
        depends_on("py-pandas", when="@0.12.3:")
        depends_on("py-psutil", when="@0.12.3:")
        depends_on("py-ubiquerg@0.4.5:", when="@0.12.3:")
        depends_on("py-yacman", when="@0.12.3:")
