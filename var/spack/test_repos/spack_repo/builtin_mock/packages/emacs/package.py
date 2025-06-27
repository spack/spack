# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
from spack_repo.builtin_mock.build_systems.generic import Package

from spack.package import *


class Emacs(Package):
    """Mock package to test adding a link dependency on a compiler, depending on a variant"""

    homepage = "http://www.example.org"
    url = "http://bowtie-1.2.2.tar.bz2"

    version("1.4.0", md5="1c837ecd990bb022d07e7aab32b09847")

    variant("native", default=False, description="adds a link dep on gcc")

    depends_on("c", type="build")
    depends_on("gcc", type="link", when="+native")
