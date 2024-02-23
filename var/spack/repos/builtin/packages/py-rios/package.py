# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyRios(PythonPackage):
    """Raster I/O Simplification. A set of python modules which makes it easy
    to write raster processing code in Python. Built on top of GDAL, it
    handles the details of opening and closing files, checking alignment of
    projection and raster grid, stepping through the raster in small blocks,
    etc., allowing the programmer to concentrate on the processing involved.
    """

    homepage = "https://www.rioshome.org/en/latest/"
    url = "https://github.com/ubarsc/rios/releases/download/rios-1.4.16/rios-1.4.16.tar.gz"

    license("GPL-3.0-only")

    version("1.4.16", sha256="2f553d85ff4ff26bfda2a8c6bd3d9dcce5ace847f7d9bd2f072c8943f3758ded")
    version("1.4.15", sha256="71670508dbffcd8f5d24fbb25e6a2b7e1d23b5e899ddc78c90d403bd65981cf4")
    version("1.4.14", sha256="ea22fde3fe70004aa1ad46bd36fad58f3346e9c161ca44ac913518a6e4fcad82")
    version("1.4.13", sha256="9f99f41f20ce769101e61bc8347aa96718e6e5ac37ccb47cb3e555dc4ca83427")
    version("1.4.12", sha256="6d897488ce1ca77e470483472998afcb2eb3bb3307f392a924b85f88a16d73eb")
    version("1.4.11", sha256="b7ae5311f987b32f1afe1fabc16f25586de8d15c17a69405d1950aeada7b748e")
    version("1.4.10", sha256="6324acccc6018f9e06c40370bc366dc459890e8c09d26e0ebd245f6fd46dad71")

    variant("parallel", default=True, description="Enables the parallel processing module")

    # pip silently replaces distutils with setuptools
    depends_on("py-setuptools", type="build")
    depends_on("py-numpy", type=("build", "run"))
    depends_on("gdal+python", type=("build", "run"))
    depends_on("py-cloudpickle", type=("build", "run"), when="@1.4.16:+parallel")
