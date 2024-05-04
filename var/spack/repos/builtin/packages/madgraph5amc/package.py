# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import os

from spack.package import *


class Madgraph5amc(MakefilePackage):
    """MadGraph5_aMC@NLO is a framework that aims at providing
    all the elements necessary for SM and BSM phenomenology,
    such as the computations of cross sections, the generation
    of hard events and their matching with event generators,
    and the use of a variety of tools relevant to
    event manipulation and analysis."""

    homepage = "https://launchpad.net/mg5amcnlo"
    url = "https://launchpad.net/mg5amcnlo/2.0/2.7.x/+download/MG5_aMC_v2.7.3.tar.gz"

    tags = ["hep"]

    # Versions from github are not recommended by the authors, see https://github.com/spack/spack/pull/41128#issuecomment-2077343326
    version(
        "3.5.4",
        sha256="19121a4b8b4ccaddd86b5b87188e91da25b755e789663c790481bf387154c950",
        url="https://github.com/mg5amcnlo/mg5amcnlo/archive/refs/tags/v3.5.4.tar.gz",
    )
    version(
        "2.9.19",
        sha256="e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855",
        preferred=True,
    )
    version("2.9.17", sha256="24026a534344c77a05b23a681437f825c41dc70c5bae5b7f79bb99e149d966b8")
    version(
        "2.8.1",
        sha256="acda34414beba201e529b8c03f87f4893fb3f99ed2956a131d60a387e76c5b8c",
        url="https://launchpad.net/mg5amcnlo/2.0/2.8.x/+download/MG5_aMC_v2.8.1.tar.gz",
        deprecated=True,
    )
    version(
        "2.7.3.py3",
        sha256="400c26f9b15b07baaad9bd62091ceea785c2d3a59618fdc27cad213816bc7225",
        url="",
        deprecated=True,
    )

    variant(
        "atlas",
        default=False,
        description="Apply changes requested by " + "the ATLAS experimenent on LHC",
    )
    variant("ninja", default=False, description="Use external installation" + " of Ninja")
    variant("collier", default=False, description="Use external installation" + " of Collier")
    variant("pythia8", default=False, description="Use external installation of Pythia8")

    conflicts("%gcc@10:", when="@2.7.3")

    depends_on("syscalc")
    depends_on("gosam-contrib", when="+ninja")
    depends_on("collier", when="+collier")
    depends_on("lhapdf")
    depends_on("fastjet")
    depends_on("py-six", when="@2.7.3.py3,2.8.0:", type=("build", "run"))

    depends_on("python@3.7:", when="@2.7.3.py3", type=("build", "run"))
    depends_on("libtirpc")
    depends_on("pythia8", when="+pythia8")

    patch("madgraph5amc-3.patch", when="@3")
    patch("array-bounds.patch", when="@:2.9")
    patch("madgraph5amc.patch", level=0, when="@:2.9")
    patch("madgraph5amc-2.7.3.atlas.patch", level=0, when="@2.7.3.py3+atlas")
    patch("madgraph5amc-2.8.0.atlas.patch", level=0, when="@2.8.0+atlas")
    patch("madgraph5amc-2.8.0.atlas.patch", level=0, when="@2.8.1+atlas")
    # Fix running from CVMFS on AFS, for example on lxplus at CERN
    patch(
        "https://patch-diff.githubusercontent.com/raw/mg5amcnlo/mg5amcnlo/pull/96.diff",
        sha256="81cc5d235a0f3ad816863afc965cbb40056b9ae26cab89c118e48548003914df",
    )

    def edit(self, spec, prefix):
        def set_parameter(name, value):
            config_files.filter(
                "^#?[ ]*" + name + "[ ]*=.*$", name + " = " + value, ignore_absent=True
            )

        config_files = FileFilter(
            join_path("input", ".mg5_configuration_default.txt"),
            join_path("input", "mg5_configuration.txt"),
        )

        set_parameter("syscalc_path", spec["syscalc"].prefix.bin)

        if "+ninja" in spec:
            set_parameter("ninja", spec["gosam-contrib"].prefix)

        if "+collier" in spec:
            set_parameter("collier", spec["collier"].prefix.lib)

        set_parameter("output_dependencies", "internal")
        set_parameter("lhapdf", join_path(spec["lhapdf"].prefix.bin, "lhapdf-config"))
        set_parameter("fastjet", join_path(spec["fastjet"].prefix.bin, "fastjet-config"))

        set_parameter("automatic_html_opening", "False")

    def build(self, spec, prefix):
        with working_dir(join_path("vendor", "CutTools")):
            make(parallel=False)

        if "+atlas" in spec:
            if os.path.exists(join_path("bin", "compile.py")):
                compile_py = Executable(join_path("bin", "compile.py"))
            else:
                compile_py = Executable(join_path("bin", ".compile.py"))

            compile_py()

    def install(self, spec, prefix):
        def installdir(dirname):
            install_tree(dirname, join_path(prefix, dirname))

        def installfile(filename):
            install(filename, join_path(prefix, filename))

        for p in os.listdir(self.stage.source_path):
            if os.path.isdir(p):
                installdir(p)
            else:
                if p != "doc.tgz":
                    installfile(p)
                else:
                    mkdirp(prefix.share)
                    install(p, join_path(prefix.share, p))

        install(
            join_path("Template", "LO", "Source", ".make_opts"),
            join_path(prefix, "Template", "LO", "Source", "make_opts"),
        )

        if "pythia8" in spec:
            with open("install-pythia8-interface", "w") as f:
                f.write(
                    f"""set pythia8_path {spec['pythia8'].prefix}
                        install mg5amc_py8_interface
                """
                )
            mg5 = Executable(join_path(prefix, "bin", "mg5_aMC"))
            mg5("install-pythia8-interface")
