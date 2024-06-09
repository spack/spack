# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Geomodel(CMakePackage):
    """GeoModel is a user-friendly C++ Toolkit and Suite for
    HEP Detector Description with minimal dependencies."""

    homepage = "https://gitlab.cern.ch/GeoModelDev/GeoModel"
    url = "https://gitlab.cern.ch/GeoModelDev/GeoModel/-/archive/4.6.0/GeoModel-4.6.0.tar.bz2"
    git = "https://gitlab.cern.ch/GeoModelDev/GeoModel"

    maintainers("wdconinc")

    license("Apache-2.0", checked_by="wdconinc")

    version("4.6.0", sha256="d827dc79a5555fd7b09d1b670fc6f01f91476d0edf98ccd644c624f18fb729ca")

    variant(
        "visualization", default=False, description="Enable the build of GeoModelVisualization"
    )
    variant("geomodelg4", default=False, description="Enable the build of GeoModelG4")
    variant("fullsimlight", default=False, description="Enable the build of FullSimLight")
    variant("fsl", default=False, description="Enable the build of FSL and FullSimLight")
    variant("examples", default=False, description="Enable the build of GeoModelExamples")
    variant("tools", default=False, description="Enable the build of GeoModelTools")
    variant(
        "hepmc3",
        default=False,
        description="Build GeoModel tools with support for the HepMC3 exchange format",
        when="+fullsimlight",
    )
    variant(
        "pythia",
        default=False,
        description="Build GeoModel tools with support for the Pythia event generator",
        when="+fullsimlight",
    )

    conflicts("+fullsimlight", when="+fsl", msg="FSL triggers the build of the FullSimLight")

    depends_on("cmake@3.16:", type="build")

    depends_on("eigen@3.2.9:")
    depends_on("nlohmann-json@3.6.1:")
    depends_on("sqlite@3.7.17:")
    depends_on("xerces-c@3.2.3:")

    depends_on("geant4", when="+geomodelg4")
    depends_on("geant4", when="+fullsimlight")
    depends_on("hepmc3", when="+hepmc3")
    depends_on("pythia8", when="+pythia")
    with when("+visualization"):
        depends_on("hdf5")
        depends_on("qt-base +gui +opengl +sql +widgets")
        depends_on("opengl")

    def cmake_args(self):
        def cmake_variant(cmake_label, spack_variant):
            enabled = spec.satisfies("+" + spack_variant)
            return f"-DGEOMODEL_BUILD_{cmake_label}={enabled}"

        args = [
            cmake_variant("VISUALIZATION", "visualization"),
            cmake_variant("GEOMODELG4", "geomodelg4"),
            cmake_variant("FULLSIMLIGHT", "fullsimlight"),
            cmake_variant("FSL", "fsl"),
            cmake_variant("EXAMPLES", "examples"),
            cmake_variant("TOOLS", "tools"),
        ]
        return args
