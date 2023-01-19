# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *
from spack.pkg.builtin.gromacs import Gromacs


class GromacsChainCoordinate(Gromacs):
    """
    A modification of GROMACS that implements the "chain coordinate", a reaction
    coordinate for pore formation in membranes and stalk formation between membranes.
    """

    homepage = "https://gitlab.com/cbjh/gromacs-chain-coordinate/-/blob/main/README.md"
    url = "https://gitlab.com/cbjh/gromacs-chain-coordinate/-/archive/release-2021.chaincoord-0.2/gromacs-chain-coordinate-release-2021.chaincoord-0.2.tar.bz2"
    git = "https://gitlab.com/cbjh/gromacs-chain-coordinate.git"
    maintainers = ["w8jcik"]

    disinherit("versions")
    version("main", branch="main")
    version(
        "2021.5-0.2",
        sha256="33dda1e39cd47c5ae32b5455af8534225d3888fd7e4968f499b8483620fa770a",
        url="https://gitlab.com/cbjh/gromacs-chain-coordinate/-/archive/release-2021.chaincoord-0.2/gromacs-chain-coordinate-release-2021.chaincoord-0.2.tar.bz2",
    )
    version(
        "2021.2-0.1",
        sha256="879fdd04662370a76408b72c9fbc4aff60a6387b459322ac2700d27359d0dd87",
        url="https://gitlab.com/cbjh/gromacs-chain-coordinate/-/archive/release-2021.chaincoord-0.1/gromacs-chain-coordinate-release-2021.chaincoord-0.1.tar.bz2",
    )

    conflicts("+plumed")

    def check(self):
        """The default 'test' targets does not compile the test programs"""
        with working_dir(self.build_directory):
            if self.generator == "Unix Makefiles":
                self._if_make_target_execute("check")
            elif self.generator == "Ninja":
                self._if_ninja_target_execute("check")
