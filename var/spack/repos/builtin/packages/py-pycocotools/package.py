# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyPycocotools(PythonPackage):
    """Official APIs for the MS-COCO dataset."""

    homepage = "https://github.com/cocodataset/cocoapi"
    pypi = "pycocotools/pycocotools-2.0.2.tar.gz"

    version("2.0.6", sha256="7fe089b05cc18e806dcf3bd764708d86dab922a100f3734eb77fb77a70a1d18c")
    version("2.0.2", sha256="24717a12799b4471c2e54aa210d642e6cd4028826a1d49fcc2b0e3497e041f1a")

    depends_on("python", type=("build", "link", "run"))
    depends_on("py-cython@0.27.3:", when="@2.0.4:", type="build")
    depends_on("py-cython@0.27.3:", when="@:2.0.3", type=("build", "run"))
    depends_on("py-setuptools@43:", when="@2.0.4:", type="build")
    depends_on("py-setuptools@18.0:", when="@:2.0.3", type=("build", "run"))
    depends_on("py-matplotlib@2.1.0:", type=("build", "run"))
    depends_on("py-numpy", type=("build", "link", "run"))
