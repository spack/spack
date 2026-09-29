# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack_repo.builtin_mock.build_systems.generic import Package

from spack.package import *


class SingleLanguageVirtual(Package):
    """Package using a single language virtual for compilation"""

    homepage = "http://www.example.com"
    url = "http://www.example.com/foo-1.0.tar.gz"

    version("1.0", md5="0123456789abcdef0123456789abcdef")

    variant("c", default=False)
    variant("cxx", default=False)
    variant("fortran", default=False)

    depends_on("c", when="+c")
    depends_on("cxx", when="+cxx")
    depends_on("fortran", when="+fortran")
