# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.build_systems import autotools, cmake
from spack.package import *


class Proj(CMakePackage, AutotoolsPackage):
    """PROJ is a generic coordinate transformation software, that transforms
    geospatial coordinates from one coordinate reference system (CRS) to
    another. This includes cartographic projections as well as geodetic
    transformations."""

    homepage = "https://proj.org/"
    url = "https://download.osgeo.org/proj/proj-7.2.1.tar.gz"

    maintainers("adamjstewart")

    # Version 6 removes projects.h, while version 7 removes proj_api.h.
    # Many packages that depend on proj do not yet support the newer API.
    # See https://github.com/OSGeo/PROJ/wiki/proj.h-adoption-status
    version("8.2.1", sha256="76ed3d0c3a348a6693dfae535e5658bbfd47f71cb7ff7eb96d9f12f7e068b1cf")
    version("8.2.0", sha256="de93df9a4aa88d09459ead791f2dbc874b897bf67a5bbb3e4b68de7b1bdef13c")
    version("8.1.1", sha256="82f1345e5fa530c407cb1fc0752e83f8d08d2b98772941bbdc7820241f7fada2")
    version("8.1.0", sha256="22c5cdc5aa0832077b16c95ebeec748a0942811c1c3438c33d43c8d2ead59f48")
    version("8.0.1", sha256="e0463a8068898785ca75dd49a261d3d28b07d0a88f3b657e8e0089e16a0375fa")
    version("8.0.0", sha256="aa5d4b934450149a350aed7e5fbac880e2f7d3fa2f251c26cb64228f96a2109e")
    version("7.2.1", sha256="b384f42e5fb9c6d01fe5fa4d31da2e91329668863a684f97be5d4760dbbf0a14")
    version("7.2.0", sha256="2957798e5fe295ff96a2af1889d0428e486363d210889422f76dd744f7885763")
    version("7.1.0", sha256="876151e2279346f6bdbc63bd59790b48733496a957bccd5e51b640fdd26eaa8d")
    version("7.0.1", sha256="a7026d39c9c80d51565cfc4b33d22631c11e491004e19020b3ff5a0791e1779f")
    version("7.0.0", sha256="ee0e14c1bd2f9429b1a28999240304c0342ed739ebaea3d4ff44c585b1097be8")
    version("6.3.2", sha256="cb776a70f40c35579ae4ba04fb4a388c1d1ce025a1df6171350dc19f25b80311")
    version("6.3.1", sha256="6de0112778438dcae30fcc6942dee472ce31399b9e5a2b67e8642529868c86f8")
    version("6.2.0", sha256="b300c0f872f632ad7f8eb60725edbf14f0f8f52db740a3ab23e7b94f1cd22a50")
    version("6.1.0", sha256="676165c54319d2f03da4349cbd7344eb430b225fe867a90191d848dc64788008")
    version("6.0.0", sha256="4510a2c1c8f9056374708a867c51b1192e8d6f9a5198dd320bf6a168e44a3657")
    version("5.2.0", sha256="ef919499ffbc62a4aae2659a55e2b25ff09cccbbe230656ba71c6224056c7e60")
    version("5.1.0", sha256="6b1379a53317d9b5b8c723c1dc7bf2e3a8eb22ceb46b8807a1ce48ef65685bb3")
    version("5.0.1", sha256="a792f78897482ed2c4e2af4e8a1a02e294c64e32b591a635c5294cb9d49fdc8c")
    version("4.9.2", sha256="60bf9ad1ed1c18158e652dfff97865ba6fb2b67f1511bc8dceae4b3c7e657796")
    version("4.9.1", sha256="fca0388f3f8bc5a1a803d2f6ff30017532367992b30cf144f2d39be88f36c319")
    version("4.8.0", sha256="2db2dbf0fece8d9880679154e0d6d1ce7c694dd8e08b4d091028093d87a9d1b5")
    version("4.7.0", sha256="fc5440002a496532bfaf423c28bdfaf9e26cc96c84ccefcdefde911efbd98986")
    version("4.6.1", sha256="76d174edd4fdb4c49c1c0ed8308a469216c01e7177a4510b1b303ef3c5f97b47")

    variant("tiff", default=True, description="Enable TIFF support")
    variant("curl", default=True, description="Enable curl support")

    # https://github.com/OSGeo/PROJ#distribution-files-and-format
    # https://github.com/OSGeo/PROJ-data
    resource(
        name="proj-data",
        url="https://download.osgeo.org/proj/proj-data-1.4.tar.gz",
        sha256="76960d34d635aa127058ce654d89ea0eff91e2e4f2036482e677af5a88669b08",
        placement="nad",
        when="@7.2.1:",
    )
    resource(
        name="proj-data",
        url="https://download.osgeo.org/proj/proj-data-1.3.tar.gz",
        sha256="0faa3e5ca6d816c907868c1ab2523668ccad27c6c4af9c7b00df9e4c3eb84398",
        placement="nad",
        when="@7.2.0",
    )
    resource(
        name="proj-data",
        url="https://download.osgeo.org/proj/proj-data-1.1.tar.gz",
        sha256="df7c57e60f9e1d5bcc724f1def71d2a7cd33bd83c28f4b4bb71dbb2d8849c84a",
        placement="nad",
        when="@7:7.1",
    )

    # https://github.com/OSGeo/PROJ#distribution-files-and-format
    # https://github.com/OSGeo/proj-datumgrid
    resource(
        name="proj-datumgrid",
        url="https://download.osgeo.org/proj/proj-datumgrid-1.8.tar.gz",
        sha256="3ff6618a0acc9f0b9b4f6a62e7ff0f7bf538fb4f74de47ad04da1317408fcc15",
        placement="nad",
        when="@:6",
    )

    # https://proj.org/install.html#build-requirements
    depends_on("googletest", when="@6:")
    depends_on("sqlite@3.11:", when="@6:")
    depends_on("libtiff@4.0:", when="@7:+tiff")
    depends_on("curl@7.29.0:", when="@7:+curl")
    depends_on("pkgconfig@0.9.0:", type="build", when="@6: build_system=autotools")
    depends_on("cmake@2.6.0:", type="build", when="build_system=cmake")

    build_system("autotools", conditional("cmake", when="@5.0.0:"), default="cmake")

    def setup_run_environment(self, env):
        # PROJ_LIB doesn't need to be set. However, it may be set by conda.
        # If an incompatible version of PROJ is found in PROJ_LIB, it can
        # cause the package to fail at run-time. See the following for details:
        # * https://proj.org/usage/environmentvars.html
        # * https://rasterio.readthedocs.io/en/latest/faq.html
        env.set("PROJ_LIB", self.prefix.share.proj)

    def setup_dependent_run_environment(self, env, dependent_spec):
        self.setup_run_environment(env)


class Setup:
    def setup_dependent_build_environment(self, env, dependent_spec):
        self.pkg.setup_run_environment(env)

    def setup_build_environment(self, env):
        env.set("PROJ_LIB", join_path(self.pkg.stage.source_path, "nad"))


class CMakeBuilder(cmake.CMakeBuilder, Setup):
    def cmake_args(self):
        args = [
            self.define_from_variant("ENABLE_TIFF", "tiff"),
            self.define_from_variant("ENABLE_CURL", "curl"),
        ]
        if self.spec.satisfies("@6:"):
            args.append(self.define("USE_EXTERNAL_GTEST", True))
        return args


class AutotoolsBuilder(autotools.AutotoolsBuilder, Setup):
    def configure_args(self):
        args = []

        if self.spec.satisfies("@6:"):
            args.append("--with-external-gtest")

        if self.spec.satisfies("@7:"):
            if "+tiff" in self.spec:
                args.append("--enable-tiff")
            else:
                args.append("--disable-tiff")

            if "+curl" in self.spec:
                args.append("--with-curl=" + self.spec["curl"].prefix.bin.join("curl-config"))
            else:
                args.append("--without-curl")

        return args
