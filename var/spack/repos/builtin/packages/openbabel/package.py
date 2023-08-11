# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Openbabel(CMakePackage):
    """Open Babel is a chemical toolbox designed to speak the many languages
    of chemical data. It's an open, collaborative project allowing anyone to
    search, convert, analyze, or store data from molecular modeling, chemistry,
    solid-state materials, biochemistry, or related areas."""

    homepage = "https://openbabel.org/wiki/Main_Page"
    url = "https://github.com/openbabel/openbabel/archive/openbabel-3-0-0.tar.gz"
    git = "https://github.com/openbabel/openbabel.git"

    maintainers("RMeli")

    version("master", branch="master")
    version("3.1.1", tag="openbabel-3-1-1")
    version("3.1.0", tag="openbabel-3-1-0")
    version("3.0.0", tag="openbabel-3-0-0")
    version("2.4.1", tag="openbabel-2-4-1")
    version("2.4.0", tag="openbabel-2-4-0")

    variant("python", default=True, description="Build Python bindings")
    variant("gui", default=True, description="Build with GUI")
    variant("cairo", default=True, description="Build with Cairo (PNG output support)")
    variant("openmp", default=False, description="Build with OpenMP")
    variant("maeparser", default=False, description="Built with MAE parser")
    variant("coordgen", default=False, description="Build with Coordgen")

    extends("python", when="+python")

    depends_on("python", type=("build", "run"), when="+python")
    depends_on("cmake@3.1:", type="build")
    depends_on("pkgconfig", type="build")
    depends_on("swig@2.0:", type="build", when="+python")

    depends_on("boost +filesystem +iostreams +test")
    depends_on("cairo", when="+cairo")  # required to support PNG depiction
    depends_on("pango", when="+cairo")  # custom cairo requires custom pango
    depends_on("eigen@3.0:")  # required if using the language bindings
    depends_on("libxml2")  # required to read/write CML files, XML formats
    depends_on("zlib-api")  # required to support reading gzipped files
    depends_on("rapidjson")  # required to support JSON
    depends_on("libsm")
    depends_on("uuid")

    depends_on("maeparser", when="+maeparser")
    depends_on("coordgen", when="+coordgen")

    # Needed for Python 3.6 support
    patch("python-3.6-rtld-global.patch", when="@:2.4.1+python")

    # Convert tabs to spaces. Allows unit tests to pass
    patch("testpdbformat-tabs-to-spaces.patch", when="@:2.4.1")

    def cmake_args(self):
        spec = self.spec
        args = []

        if "+python" in spec:
            args.extend(
                [
                    "-DPYTHON_BINDINGS=ON",
                    "-DPYTHON_EXECUTABLE={0}".format(spec["python"].command.path),
                    "-DRUN_SWIG=ON",
                ]
            )
        else:
            args.append("-DPYTHON_BINDINGS=OFF")

        args.append(self.define_from_variant("BUILD_GUI", "gui"))
        args.append(self.define_from_variant("ENABLE_OPENMP", "openmp"))
        args.append(self.define_from_variant("WITH_MAEPARSER", "maeparser"))
        args.append(self.define_from_variant("WITH_COORDGEN", "coordgen"))

        return args

    @run_after("install")
    @on_package_attributes(run_tests=True)
    def check_install(self):
        obabel = Executable(join_path(self.prefix.bin, "obabel"))
        obabel("-:C1=CC=CC=C1Br", "-omol")

        if "+python" in self.spec:
            python("-c", "import openbabel")
            if self.spec.version < Version("3.0.0"):
                python("-c", "import pybel")
