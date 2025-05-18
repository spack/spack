# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyDeprecat(PythonPackage):
    """Python @deprecat decorator to deprecate old python classes, functions or methods."""

    homepage = "https://github.com/mjhajharia/deprecat"
    pypi = "deprecat/deprecat-2.1.3.tar.gz"

    license("MIT")

    version("2.1.3", sha256="d93cdd493af68981f0c7d198c2b9df2358ead5e54ce3e671a3522af8785917e8")

    depends_on("py-setuptools", type="build")
    depends_on("py-wrapt@1.10:1", type=("build", "run"))
