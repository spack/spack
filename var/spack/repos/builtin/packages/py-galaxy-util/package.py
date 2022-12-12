# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class PyGalaxyUtil(PythonPackage):
    """Galaxy Generic Utilities"""

    homepage = "https://github.com/galaxyproject/galaxy"

    version(
        "22.1.2",
        url="https://files.pythonhosted.org/packages/c6/6b/ca93c7a73a1d9c2153592007fd8264a357cb277de8d980ab6aa91c9cc8d1/galaxy_util-22.1.2-py2.py3-none-any.whl",
        sha256="23c9ea814244dfb020e30ea3284d6dacfd9ba4119fb76c1cc2b3ab379463f43c",
        expand=False,
    )

    depends_on("python@3.7:3.10", type=("build", "run"))
    depends_on("py-setuptools", type="build")

    depends_on("py-boltons", type=("build", "run"))
