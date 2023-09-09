# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Garfieldpp(CMakePackage):
    """Garfield++ is a toolkit for the detailed simulation of particle
    detectors based on ionisation measurement in gases and semiconductors."""

    homepage = "https://garfieldpp.web.cern.ch/garfieldpp/"
    url = "https://gitlab.cern.ch/garfield/garfieldpp/-/archive/4.0/garfieldpp-4.0.tar.gz"
    git = "https://gitlab.cern.ch/garfield/garfieldpp.git"

    tags = ["hep"]

    maintainers("mirguest")
    # ###################### Patches ##########################
    patch("https://gitlab.cern.ch/garfield/garfieldpp/-/commit/882c3023cfa89b45ca7a0c95ab1518454536e8e1.patch",
          sha256="440bc8129c55168e6c45d39e4344911d48ddb13fd3f9ee05974b2ede46a23b93",
          when="@:4.0")

    # ###################### Variants ##########################
    variant("examples", default=False, description="Build garfield examples")

    # ###################### Versions ##########################
    version("master", branch="master")
    version("4.0", sha256="82bc1f0395213bd30a7cd854426e6757d0b4155e99ffd4405355c9648fa5ada3")
    version("3.0", sha256="c1282427a784658bc38b71c8e8cfc8c9f5202b185f0854d85f7c9c5a747c5406")

    depends_on("root")
    depends_on("gsl")
    depends_on("geant4", when="+examples")

    def cmake_args(self):
        args = [self.define_from_variant("WITH_EXAMPLES", "examples")]
        return args
