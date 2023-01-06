# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *
from spack.pkg.builtin.kokkos import Kokkos


class Exaca(CMakePackage):
    """ExaCA: an exascale cellular automata application for alloy solidification modeling"""

    homepage = "https://github.com/LLNL/ExaCA"
    git = "https://github.com/LLNL/ExaCA.git"
    url = "https://github.com/LLNL/ExaCA/archive/1.0.0.tar.gz"

    maintainers = ["streeve", "MattRolchigo"]

    tags = ["ecp"]

    version("master", branch="master")
    version("1.0.0", sha256="48556233360a5e15e1fc20849e57dd60739c1991c7dfc7e6b2956af06688b96a")

    _kokkos_backends = Kokkos.devices_variants
    for _backend in _kokkos_backends:
        _deflt, _descr = _kokkos_backends[_backend]
        variant(_backend.lower(), default=_deflt, description=_descr)

    variant("shared", default=True, description="Build shared libraries")
    variant("testing", default=False, description="Build unit tests")

    depends_on("cmake@3.9:", type="build")
    depends_on("googletest@1.10:", type="build", when="@master+testing")
    depends_on("kokkos@3.0:")
    depends_on("mpi")

    def cmake_args(self):
        options = [self.define_from_variant("BUILD_SHARED_LIBS", "shared")]

        if self.spec.satisfies("@master"):
            options += [self.define_from_variant("ExaCA_ENABLE_TESTING", "testing")]

        return options
