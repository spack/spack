# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class Estarlight(CMakePackage):
    """Monte Carlo event generator for coherent vector meson photo- and electro-
    production in electron-ion collisions."""

    homepage = "https://github.com/eic/estarlight"
    url = "https://github.com/eic/estarlight/archive/refs/tags/v1.0.0.zip"
    list_url = "https://github.com/eic/estarlight/releases"
    git = "https://github.com/eic/estarlight.git"

    maintainers = ["wdconinc"]

    version("master", branch="master")
    version("1.0.0", sha256="a963bd4e08218767030ddadb7ad72d8d93f2468dfdce309abf566e87326c81f4")

    variant("dpmjet", default=False, description="Use dpmjet for jets")
    variant("hepmc3", default=False, description="Support HepMC3 writing")
    variant("pythia6", default=False, description="Use Pythia6 for parton showers")
    variant("pythia8", default=False, description="Use Pythia8 for parton showers")

    depends_on("dpmjet", when="+dpmjet")
    depends_on("hepmc3", when="+hepmc3")
    depends_on("pythia6", when="+pythia6")
    depends_on("pythia8", when="+pythia8")

    def cmake_args(self):
        args = [
            self.define_from_variant("ENABLE_DPMJET", "dpmjet"),
            self.define_from_variant("ENABLE_HEPMC3", "hepmc3"),
            self.define_from_variant("ENABLE_PYTHIA6", "pythia6"),
            self.define_from_variant("ENABLE_PYTHIA", "pythia8"),
        ]
        return args
