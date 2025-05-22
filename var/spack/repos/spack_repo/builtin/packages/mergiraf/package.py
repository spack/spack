# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack_repo.builtin.build_systems.cargo import CargoPackage

from spack.package import *


class Mergiraf(CargoPackage):
    """A syntax-aware git merge driver for a growing collection of programming
    languages and file formats.
    """

    homepage = "https://mergiraf.org/"
    url = "https://codeberg.org/mergiraf/mergiraf/archive/v0.6.0.tar.gz"

    maintainers("alecbcs")

    license("GPL-3.0-only")

    version("0.6.0", sha256="548b0ae3d811d6410beae9e7294867c7e6d791cf9f68ddda5c24e287f7978030")
