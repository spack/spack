# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack_repo.builtin.build_systems.autotools import AutotoolsPackage

from spack.package import *


class Lbzip2(AutotoolsPackage):
    """Multi-threaded compression utility with support for bzip2
    compressed file format"""

    homepage = "https://github.com/kjn/lbzip2/"
    url = "https://github.com/kjn/lbzip2/archive/refs/tags/v2.5.tar.gz"

    depends_on("c", type="build")

    depends_on("autoconf", type="build")
    depends_on("automake", type="build")
    depends_on("libtool", type="build")

    version(
        "2.5",
        sha256="7be69ece83ecdc8f12b9201d838eee5cdb499f2fd68cffd2af58866076ccac43",
        deprecated=True,
    )
