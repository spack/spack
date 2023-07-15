# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyZstandard(PythonPackage):
    """Zstandard bindings for Python."""

    homepage = "https://github.com/indygreg/python-zstandard"
    pypi = "zstandard/zstandard-0.21.0.tar.gz"

    version("0.21.0", sha256="f08e3a10d01a247877e4cb61a82a319ea746c356a3786558bed2481e6c405546")

    depends_on("python@3.7:", type=("build", "run"))
    depends_on("py-setuptools", type="build")
    depends_on("py-cffi@1.11:", type=("build", "run"))
    depends_on("zstd")

    def global_options(self, spec, prefix):
        options = ["--system-zstd"]
        return options
