# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class Py(PythonPackage):
    """
    """

    homepage = ""
    pypi = ""

    version("", sha256="")

    depends_on("python", type=("build", "run"))
    depends_on("py-setuptools", type="build")

    depends_on("", type=("build", "run"))

    depends_on("", type="run")
