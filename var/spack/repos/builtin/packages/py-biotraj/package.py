# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyBiotraj(PythonPackage):
    """Reading structures from trajectory files."""

    homepage = "https://github.com/biotite-dev/biotraj"

    url = "https://github.com/biotite-dev/biotraj/archive/refs/tags/v1.2.1.tar.gz"

    license("LGPL-2.1")

    version("1.2.1", sha256="4c93641dfa138d067be8d3aeb8f07be6342ec76d450ad3ab1801a92bfdbfbf85")
    version("1.2.0", sha256="d2226348546ef384d23f608cca8f7110d1e6fa8927dcbd74dbf00ee748929cd1")

    depends_on("python@3.10:", type=("build", "run"))

    depends_on("py-setuptools@64:", type="build")
    depends_on("py-setuptools-scm@8.0:", type="build")
    depends_on("py-wheel", type="build")
    depends_on("py-cython@3.0:", type=("build", "run"))
    depends_on("py-numpy@2.0:", when="@1.2.0", type=("build", "run"))
    depends_on("py-numpy@1.25:", when="@1.2.1", type=("build", "run"))
    depends_on("py-scipy@1.13:", type=("build", "run"))
