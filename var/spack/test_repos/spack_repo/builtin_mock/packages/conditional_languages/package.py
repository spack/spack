# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
from spack_repo.builtin_mock.build_systems.generic import Package

from spack.package import *


class ConditionalLanguages(Package):
    """Conditional depends on c/cxx/fortran with a variant for each"""

    homepage = "https://dev.null"

    version("1.0")

    variant("c", default=False, description="depend on c")
    variant("cxx", default=False, description="depend on cxx")
    variant("fortran", default=False, description="depend on fortran")

    depends_on("c", type="build", when="+c")
    depends_on("cxx", type="build", when="+cxx")
    depends_on("fortran", type="build", when="+fortran")
