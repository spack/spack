# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class PyDnspython(PythonPackage):
    """DNS toolkit"""

    homepage = "https://www.dnspython.org"
    pypi = "dnspython/dnspython-2.2.1.tar.gz"

    version("2.2.1", sha256="0f7569a4a6ff151958b64304071d370daa3243d15941a7beedf0c9fe5105603e")

    depends_on("python@3.6:3", type=("build", "run"))
    depends_on("py-poetry-core", type="build")
