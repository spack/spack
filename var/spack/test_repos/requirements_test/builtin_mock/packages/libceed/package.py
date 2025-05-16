# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
from spack.package import *


class Libceed(Package):
    """Package that has a dependency imposing conditional requirements on platforms"""

    homepage = "https://github.com/CEED/libCEED"
    url = "http://www.fake.com/libceed.tgz"

    version("0.12.0", sha256="e491ccadebc5cdcd1fc08b5b4509a0aba4e2c096f53d7880062a66b82a0baf84")

    depends_on("c", type="build")
    depends_on("cxx", type="build")

    depends_on("libxsmm")
