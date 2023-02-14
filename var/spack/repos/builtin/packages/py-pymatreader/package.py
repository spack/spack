# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyPymatreader(PythonPackage):
    """Convenient reader for Matlab mat files."""

    homepage = "https://gitlab.com/obob/pymatreader"
    pypi = "pymatreader/pymatreader-0.0.30.tar.gz"

    version("0.0.30", sha256="c8187b6ee77a9b1ec0d8ccae9b22c9031d01104a412737cc4a71e6d993a1a12b")

    depends_on("py-setuptools", type="build")

    depends_on("py-h5py", type=("build", "run"))
    depends_on("py-scipy@:1.6,1.7.1:", type=("build", "run"))
    depends_on("py-numpy", type=("build", "run"))
    depends_on("py-xmltodict", type=("build", "run"))
    depends_on("py-future", type=("build", "run"))
