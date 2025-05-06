# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
from spack.package import *


class Libxsmm(Package):
    """Package that imposes conditional requirements on platforms"""

    homepage = "https://github.com/libxsmm/libxsmm"
    url = "https://github.com/libxsmm/libxsmm/archive/1.17.tar.gz"
    git = "https://github.com/libxsmm/libxsmm.git"

    version("main", branch="main")
    version("1.16.3", sha256="e491ccadebc5cdcd1fc08b5b4509a0aba4e2c096f53d7880062a66b82a0baf84")

    depends_on("c", type="build")
    depends_on("cxx", type="build")

    requires("platform=linux", "platform=test")
    requires("platform=linux", when="@:1")
