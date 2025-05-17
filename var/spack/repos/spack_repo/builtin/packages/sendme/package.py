# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack_repo.builtin.build_systems.cargo import CargoPackage

from spack.package import *


class Sendme(CargoPackage):
    """A cli tool to send directories over the network, with NAT hole punching"""

    homepage = "https://www.iroh.computer/sendme"
    git = "https://github.com/n0-computer/sendme.git"

    maintainers("draguve")

    license("Apache-2.0 OR MIT")

    version("main", branch="main")
    version("0.25.0", tag="v0.25.0", commit="b9081f52632e3190e46dd5eeeca58c8a1646f107")
    version("0.24.0", tag="v0.24.0", commit="fdb03b324cbe8d4e4ceb25c628df75f88d0edf93")
    version("0.23.0", tag="v0.23.0", commit="39f6111d8c3a973ea1f54a3c47aad07014de854b")
    depends_on("rust@1.81:", type="build")

    sanity_check_is_file = [join_path("bin", "sendme")]
