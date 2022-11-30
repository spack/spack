# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class PySpython(PythonPackage):
    """The Python API for working with Singularity containers.
    """

    homepage = "https://github.com/singularityhub/singularity-cli"
    pypi = "spython/spython-0.2.14.tar.gz"

    version("0.2.14", sha256="49e22fbbdebe456b27ca17d30061489db8e0f95e62be3623267a23b85e3ce0f0")

    depends_on("python", type=("build", "run"))
    depends_on("py-setuptools", type="build")

    depends_on("py-requests", type=("build", "run"))
    depends_on("py-semver", type=("build", "run"))
    depends_on("singularity@3.5.2:", type="run")
