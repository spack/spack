# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyEtils(PythonPackage):
    """etils (eclectic utils) is an open-source collection of utils
    for python."""

    homepage = "https://github.com/google/etils"
    pypi = "etils/etils-0.9.0.tar.gz"

    version("0.9.0", sha256="489103e9e499a566765c60458ee15d185cf0065f2060a4d16a68f8f46962ed0d")

    variant("epath", default=False, description="with epath module")

    depends_on("python@3.7:", type=("build", "run"))

    depends_on("py-importlib-resources", type=("build", "run"), when="+epath")
    depends_on("py-typing-extensions", type=("build", "run"), when="+epath")
    depends_on("py-zipp", type=("build", "run"), when="+epath")

    depends_on("py-flit-core@3.5:3", type="build")
