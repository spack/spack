# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class PyGalaxyUtil(PythonPackage):
    """Galaxy Generic Utilities"""

    homepage = "https://github.com/galaxyproject/galaxy"
    pypi = "galaxy-util/galaxy-util-22.1.2.tar.gz"

    license("CC-BY-3.0")

    version(
        "22.1.2",
        sha256="23c9ea814244dfb020e30ea3284d6dacfd9ba4119fb76c1cc2b3ab379463f43c",
        url="https://pypi.org/packages/c6/6b/ca93c7a73a1d9c2153592007fd8264a357cb277de8d980ab6aa91c9cc8d1/galaxy_util-22.1.2-py2.py3-none-any.whl",
    )

    with default_args(type="run"):
        depends_on("py-bleach")
        depends_on("py-boltons")
        depends_on("py-docutils")
        depends_on("py-importlib-resources", when="@22:")
        depends_on("py-markupsafe", when="@:22.5.0.dev0")
        depends_on("py-packaging@:21", when="@22.1.2:23.0")
        depends_on("py-pycryptodome", when="@21.9:22.5.0.dev0")
        depends_on("py-pyparsing", when="@22.1.2:")
        depends_on("py-pyyaml")
        depends_on("py-requests", when="@20.5:")
        depends_on("py-routes")
        depends_on("py-typing-extensions", when="@22:")
        depends_on("py-zipstream-new", when="@21:")
