# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyLightningCloud(PythonPackage):
    """Lightning AI Command Line Interface."""

    homepage = "https://lightning.ai/"
    pypi = "lightning_cloud/lightning_cloud-0.5.31.tar.gz"

    version("0.5.31", sha256="a5a138f4abbeffe66ee476fb9a8d621befac0434ffeeeec1cc00ccd3d72ffc09")

    depends_on("py-setuptools", type="build")
    depends_on("py-click", type=("build", "run"))
    depends_on("py-fastapi+all", type=("build", "run"))
    depends_on("py-pyjwt", type=("build", "run"))
    depends_on("py-requests", type=("build", "run"))
    depends_on("py-rich", type=("build", "run"))
    depends_on("py-six", type=("build", "run"))
    depends_on("py-urllib3", type=("build", "run"))
    depends_on("py-websocket-client", type=("build", "run"))
