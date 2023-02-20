# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class PyDamask(PythonPackage):
    """Pre- and post-processing tools for DAMASK"""

    homepage = "https://damask.mpie.de"
    url = "https://damask.mpie.de/download/damask-3.0.0.tar.xz"

    maintainers("MarDiehl")

    version(
        "3.0.0-alpha7", sha256="442b06b824441293e72ff91b211a555c5d497aedf62be1c4332c426558b848a4"
    )
    version(
        "3.0.0-alpha6", sha256="de6748c285558dec8f730c4301bfa56b4078c130ff80e3095faf76202f8d2109"
    )
    version(
        "3.0.0-alpha5", sha256="2d2b10901959c26a5bb5c52327cdafc7943bc1b36b77b515b0371221703249ae"
    )
    version(
        "3.0.0-alpha4", sha256="0bb8bde43b27d852b1fb6e359a7157354544557ad83d87987b03f5d629ce5493"
    )

    depends_on("python@3.8:", type=("build", "run"), when="@3.0.0-alpha6:")
    depends_on("python@3.7:", type=("build", "run"))
    depends_on("py-setuptools@40.6:", type="build")
    depends_on("vtk+python", type=("build", "run"))
    depends_on("py-pandas", type=("build", "run"))
    depends_on("py-scipy", type=("build", "run"))
    depends_on("py-h5py", type=("build", "run"))
    depends_on("py-matplotlib", type=("build", "run"))
    depends_on("py-pyyaml", type=("build", "run"))

    patch("setup.patch", when="@3.0.0-alpha7")

    build_directory = "python"
