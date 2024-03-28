# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class PyPydeps(PythonPackage):
    """Python module dependency visualization."""

    pypi = "pydeps/pydeps-1.7.1.tar.gz"

    version(
        "1.9.0",
        sha256="59d6d0f5a2b8ebdb11caf0439dd36ad7b918de7c8c338ba9d526b8fd700a346d",
        url="https://pypi.org/packages/0a/84/4553dfa9ba5a778f677745806a214028ef2f8e4ec20dfd7ea0a5fd52fd5d/pydeps-1.9.0-py2-none-any.whl",
    )
    version(
        "1.7.1",
        sha256="0cc20d7d0c626a3cbec611498e7a79a33898430a044e316e6c1a50567c3a353a",
        url="https://pypi.org/packages/26/a7/2af0a6e78dd1413c78d5c3ec6f9effaa654e4ec4e5afc29bcafa66479081/pydeps-1.7.1-py2-none-any.whl",
    )

    with default_args(type="run"):
        depends_on("py-stdlib-list", when="@1.3.7:")
