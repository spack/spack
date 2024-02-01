# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class Bdsim(CMakePackage):
    """Beam Delivery Simulation (BDSIM) is a C++ program that utilises the Geant4 toolkit
    to simulate both the transport of particles in an accelerator and their
    interaction with the accelerator material"""

    homepage = "http://www.pp.rhul.ac.uk/bdsim/manual/index.html"
    url = "https://bitbucket.org/jairhul/bdsim/get/v1.6.0.tar.gz"
    git = "https://bitbucket.org/jairhul/bdsim/src/master/"

    tags = ["hep"]

    maintainers("gganis")

    version("develop", branch="develop")
    version("1.6.0", sha256="e3241d2d097cb4e22249e315c1474da9b3657b9c6893232d9f9e543a5323f717")

    depends_on("cmake")
    depends_on("geant4")
    depends_on("geant4@:10.7.3", when="@:1.6.0")
    depends_on("root")
    depends_on("clhep")
    depends_on("flex")
    depends_on("bison")
