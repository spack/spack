# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Reprimand(MesonPackage):
    """RePrimAnd: Recovery of Primitives And EOS framework

    RePrimAnd is a support library for numerical simulations of general
    relativistic magnetohydrodynamics. It provides methods for recovering
    primitive variables like pressure and velocity from the variables evolved
    in quasi-conservative formulations. Further, it provides a general
    framework for handling matter equations of state."""

    homepage = "https://wokast.github.io/RePrimAnd/index.html"
    url = "https://github.com/wokast/RePrimAnd/archive/refs/tags/v1.3.tar.gz"

    maintainers = ["eschnett"]

    version("develop", git="https://github.com/wokast/RePrimAnd", branch="public")
    version("1.5", sha256="0f1d65a170cad7bc071c58b747b2f0bdc1df77e4c56c152dfb6c93a9d1360f28")
    version("1.4", sha256="7ddeb770b5b2e2826c5889a38427fa201bb6b9ff98b4ded291ea730ad0e61a42")
    version("1.3", sha256="2b9d016f0d2d3d11082f049c2b80e57a8c3ea4d5e3875a863c7c485767475ee5")

    # Add missing #include statments; see
    # <https://github.com/wokast/RePrimAnd/issues/3>
    patch("include.patch", when="@1.3")

    variant("python", default=False, description="Enable Python bindings")
    variant("shared", default=True, description="Build shared library")

    depends_on("boost +json +math +test")
    depends_on("gsl")
    depends_on("hdf5")
    depends_on("python", when="+python")
    depends_on("py-matplotlib", when="+python")
    depends_on("py-pybind11 @2.6.0:", when="+python")

    extends("python", when="+python")

    def setup_build_environment(self, env):
        env.set("CXXFLAGS", self.compiler.cxx11_flag)
        env.set("BOOST_ROOT", self.spec["boost"].prefix)

    def meson_args(self):
        args = []
        if self.spec.satisfies("@:1.4"):
            args.extend(
                [
                    "-Dbuild_documentation=false",
                    "-Dbuild_python_api={0}".format(str("+python" in self.spec).lower()),
                ]
            )
        return args

    @property
    def libs(self):
        shared = "+shared" in self.spec
        return find_libraries("libRePrimAnd*", root=self.prefix, shared=shared, recursive=True)
