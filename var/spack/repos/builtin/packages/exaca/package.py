# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
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

    maintainers("streeve", "MattRolchigo")

    tags = ["ecp"]

    version("master", branch="master")
    version("1.1.0", sha256="10106fb1836964a19bc5bab3f374baa24188ba786c768e554442ab896b31ff24")
    version("1.0.0", sha256="48556233360a5e15e1fc20849e57dd60739c1991c7dfc7e6b2956af06688b96a")

    _kokkos_backends = Kokkos.devices_variants
    for _backend in _kokkos_backends:
        _deflt, _descr = _kokkos_backends[_backend]
        variant(_backend.lower(), default=_deflt, description=_descr)

    variant("shared", default=True, description="Build shared libraries")
    variant("testing", default=False, description="Build unit tests")

    depends_on("cmake@3.9:", type="build", when="@:1.1")
    depends_on("cmake@3.12:", type="build", when="@master")
    depends_on("googletest@1.10:", type="test", when="@1.1:+testing")
    depends_on("kokkos@3.0:", when="@:1.1")
    depends_on("kokkos@3.2:", when="@master")
    depends_on("mpi")

    def cmake_args(self):
        options = [self.define_from_variant("BUILD_SHARED_LIBS", "shared")]

        if self.spec.satisfies("@1.1:"):
            options += [self.define_from_variant("ExaCA_ENABLE_TESTING", "testing")]

        return options
