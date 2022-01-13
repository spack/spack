# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.build_systems.python import PythonPackage
from spack.directives import depends_on, version


class PyAtldld(PythonPackage):
    """Search, download, and prepare brain atlas data."""

    homepage = "atlas-download-tools.rtfd.io"
    git = "https://github.com/BlueBrain/Atlas-Download-Tools.git"

    maintainers = ["EmilieDel", "jankrepl", "Stannislav"]

    version("0.3.2", tag="v0.3.2")
    version("0.3.1", tag="v0.3.1")
    version("0.3.0", tag="v0.3.0")
    version("0.2.2", tag="v0.2.2")

    # Build dependencies
    depends_on("python@3.7:", type=("build", "run"))
    depends_on("py-setuptools", type="build")
    depends_on("py-setuptools-scm", type="build")

    depends_on("py-appdirs", when="@0.3.1:", type=("build", "run"))
    depends_on("py-click@8:", when="@0.3.0:", type=("build", "run"))
    depends_on("py-dataclasses", when="@0.3.1: ^python@3.6", type=("build", "run"))
    depends_on("py-matplotlib", type=("build", "run"))
    depends_on("py-numpy", type=("build", "run"))
    depends_on("py-opencv-python", type=("build", "run"))
    depends_on("py-pandas", type=("build", "run"))
    depends_on("py-pillow", when="@0.3.1:", type=("build", "run"))
    depends_on("py-requests", type=("build", "run"))
    depends_on("py-responses", type=("build", "run"))
    depends_on("py-scikit-image", type=("build", "run"))
