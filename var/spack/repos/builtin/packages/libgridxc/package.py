# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import os

from spack.package import *


class Libgridxc(AutotoolsPackage,MakefilePackage):
    """A library to compute the exchange and correlation energy and potential
    in spherical (i.e. an atom) or periodic systems.
    """

    homepage = "https://gitlab.com/siesta-project/libraries/libgridxc"
    git = "https://gitlab.com/siesta-project/libraries/libgridxc.git"
    url = "https://gitlab.com/siesta-project/libraries/libgridxc/-/archive/libgridxc-0.9.6/libgridxc-libgridxc-0.9.6.tar.gz"

    version("master", branch="master")
    version("2.0.1", tag="2.0.1", sha256="8311c3ec164832f82255d1d487ada8a6909192e7")
    version("2.0.0", tag="2.0.0", sha256="77058d35f5f46b137ce068bba7c3ce9132764c8e")
    version("1.1.2", tag="1.1.2", sha256="f2110885d0ae508f3aa8547dc7da58ab7a6895c2")
    version("1.1.0", tag="1.1.0", sha256="b6633413d09c5286597414dd19349e5bdc15f0a4")
    version("0.9.6", sha256="3b89ccc02d65729ea2d7cb291ae1d9b53acd65c1fd144e8846362cffb71b114a")
    version("0.9.5", sha256="98aa34dbaffe360ff332606eebb7c842994244a3114015d89c5a3850298c40aa")
    version("0.9.1", sha256="346735e30dd3a4099532a985b7a491f6d2b882954a527bdac655d87232be5341")
    version("0.8.5", sha256="af293be83d85908231aba9074f2b51545457bc7fce87fab9f72010a10f0028a6")
    version("0.8.4", sha256="b4f2f4af1f0c98b9e82505b99924da16e8c7719dd3e3e95f1d16e504b43944ce")
    version("0.8.3", sha256="01643c2e009474d4eb1f945f7e506f465bf0378d19e56028bc4a9af56ab0b1f3")
    version("0.8.0", sha256="ff89b3302f850d1d9f651951e4ade20dfa4c71c809a2d86382c6797392064c9c")
    version("0.7.6", sha256="058b80f40c85997eea0eae3f15b7cc8105f817e59564106308b22f57a03b216b")

    build_system(conditional("autotools", when="@1.1.0:"), "makefile", default="autotools")

    variant("mpi", default=False, description="Build with MPI support")

    depends_on("mpi", when="+mpi")
    depends_on("autoconf@2.69:", type="build")
    depends_on("automake@1.14:", type="build")
    depends_on("libtool@2.4.2:", type="build")
    depends_on("m4", type="build")
    depends_on("libxc@:4.3.4", when="@0.8.0:")

    build_directory = "build"

    parallel = False

    @property
    def build_targets(self):
        args = ["PREFIX={0}".format(self.prefix), "FC=fc"]

    def edit(self, spec, prefix):
        sh = which("sh")
        with working_dir("build", create=True):
            sh("../src/config.sh")
            copy("../extra/fortran.mk", "fortran.mk")

    def configure_args(self):
        args = ["--prefix={0}".format(self.prefix)]
        if self.spec.satisfies("@0.8.0:"):
            args += ["WITH_LIBXC=1", "LIBXC_ROOT={0}".format(self.spec["libxc"].prefix)]
        if self.spec.satisfies("+mpi"):
            args += ["--enable-multiconfig", "--with-mpi"]
            args += ["CC={0}".format(self.spec["mpi"].mpicc)]
            args += ["FC={0}".format(self.spec["mpi"].mpifc)]
        else:
            args.append("FC=fc")
        if self.spec.satisfies("%fj"):
            args += ["--enable-nec-compat"]
        return args

    @when("@:0.9.6")
    def install(self, spec, prefix):
        mkdirp(join_path(self.prefix, "share", "org.siesta-project"))
        install(
            join_path(self.prefix, "gridxc.mk"),
            join_path(self.prefix, "share", "org.siesta-project", "gridxc.mk"),
        )
        os.remove(join_path(self.prefix, "gridxc.mk"))
        install(
            join_path(self.prefix, "libxc.mk"),
            join_path(self.prefix, "share", "org.siesta-project", "libxc.mk"),
        )
        os.remove(join_path(self.prefix, "libxc.mk"))
