# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyTriangle(PythonPackage):
    """Python bindings to the triangle library"""

    homepage = "https://github.com/drufat/triangle"
    pypi = "triangle/triangle-20200424.tar.gz"

    version("20200424", sha256="fc207641f8f39986f7d2bee1b91688a588cd235d2e67777422f94e61fece27e9")

    depends_on("py-setuptools", type="build")
    depends_on("triangle", type=("build", "run"))
    depends_on("py-numpy", type=("build", "run"))
    depends_on("py-cython", type=("build"))
