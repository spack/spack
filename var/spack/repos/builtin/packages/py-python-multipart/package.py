# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class PyPythonMultipart(PythonPackage):
    """A streaming multipart parser for Python"""

    homepage = "https://github.com/andrew-d/python-multipart"
    pypi = "python-multipart/python-multipart-0.0.5.tar.gz"

    license("Apache-2.0")

    version("0.0.5", sha256="f7bb5f611fc600d15fa47b3974c8aa16e93724513b49b5f95c81e6624c83fa43")

    depends_on("py-setuptools", type="build")

    depends_on("py-six@1.4.0:", type=("build", "run"))
