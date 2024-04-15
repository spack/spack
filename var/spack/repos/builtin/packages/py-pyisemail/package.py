# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyPyisemail(PythonPackage):
    """pyIsEmail is a no-nonsense approach for checking whether that user-supplied
    email address could be real."""

    homepage = "https://github.com/michaelherold/pyIsEmail"
    pypi = "pyisemail/pyisemail-2.0.1.tar.gz"

    maintainers("meyersbs")

    license("MIT")

    version(
        "2.0.1",
        sha256="3d2bebd159f436673219d024a3f02bed1b468c793df9a5fa08d72b7d4b4f6cb4",
        url="https://pypi.org/packages/11/d2/d62d675754a40ec41cd3c28417b6707278de5490d4da1cf7d79da61ebaa1/pyisemail-2.0.1-py3-none-any.whl",
    )

    with default_args(type=("build", "run")):
        depends_on("python@3.7:", when="@2:")
        depends_on("py-dnspython@2.0.0:", when="@2:")
