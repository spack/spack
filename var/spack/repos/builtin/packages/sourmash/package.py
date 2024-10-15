# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Sourmash(PythonPackage):
    """Sourmash: Quickly search, compare, and analyze genomic and metagenomic data sets with
    k-mer sketches."""

    homepage = "https://sourmash.bio/"
    pypi = "sourmash/sourmash-4.8.4.tar.gz"
    git = "https://github.com/sourmash-bio/sourmash.git"

    maintainers("luizirber")

    version("4.8.2", sha256="e0df78032e53ed88977445933ba3481dd10c7d3bd26d019511a6a4e6d7518475")
    version("4.8.4", sha256="43584c112c3310719771de175b89cba94f1c2d30b1aea46000eaf5a81efbae8a")

    depends_on("python@3.8:", type=("build", "run"))
    # build-only
    depends_on("py-maturin@0.14.13:0.14", when="@4.8.2:", type="build")
    depends_on("py-maturin@1", when="@4.8.4:", type="build")
    depends_on("rust", type="build")
    # general
    depends_on("py-screed@1.1.2:1", type=("build", "run"))
    depends_on("py-cffi@1.15.1:", when="@4.8.4:", type=("build", "run"))
    depends_on("py-cffi@1.14.0:", when="@4.8.2:", type=("build", "run"))
    depends_on("py-numpy", type=("build", "run"))
    depends_on("py-matplotlib", type=("build", "run"))
    depends_on("py-scipy", type=("build", "run"))
    depends_on("py-deprecation@2.0.6:", type=("build", "run"))
    depends_on("py-cachetools@4:5", type=("build", "run"))
    depends_on("py-bitstring@3.1.9:4", type=("build", "run"))
    depends_on("py-importlib_metadata@3.6:", when="^python@:3.9", type=("build", "run"))

    def install(self, spec, prefix):
        # build rust libs
        cargo = Executable("cargo")
        cargo("build", "--release")
        # install python package
        args = std_pip_args + ["--prefix=" + prefix, "."]
        pip(*args)
        # move sourmash.so into expected place
        site_packages = join_path(python_platlib, "sourmash")
        lib_ext = "dylib" if spec.platform == "Darwin" else "so"
        install(
            join_path("target", "release", "libsourmash.{}".format(lib_ext)),
            join_path(site_packages, "_lowlevel__lib.so"),
        )
