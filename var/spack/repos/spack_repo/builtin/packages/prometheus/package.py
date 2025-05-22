# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack_repo.builtin.build_systems.makefile import MakefilePackage

from spack.package import *


class Prometheus(MakefilePackage):
    """Prometheus, a Cloud Native Computing Foundation project, is a
    systems and service monitoring system."""

    homepage = "https://prometheus.io/"
    url = "https://github.com/prometheus/prometheus/archive/refs/tags/v2.55.1.tar.gz"

    license("Apache-2.0")

    version("2.55.1", sha256="f48251f5c89eea6d3b43814499d558bacc4829265419ee69be49c5af98f79573")
    version("2.19.2", sha256="f77017846259d01f281ded0d70af834e06ee489d325c9c84de0e68c7d505b42b")
    version("2.19.1", sha256="c5bdfb3653b82c1d26e5e14feadf644692289fae42a48e2567629aa2c4a02fc4")
    version("2.18.2", sha256="01b4d55aae0a43c9eecb5a660648e45e74ea20f9d4558ff6533058f2050aabd1")
    version("2.17.1", sha256="443590c1896cf5096b75d4a30e45381c84a5d17712dc714109ea8cf418b275ac")
    version("2.17.0", sha256="c94b13677003838d795c082b95878903d43cd21ab148996d39f1900f00370c97")

    depends_on("c", type="build")  # generated

    depends_on("go@1.17:", type="build", when="@2.37.0:")
    depends_on("go@1.16:", type="build", when="@2.33.0:")
    depends_on("go@1.14:", type="build", when="@2.23.0:")
    depends_on("go@1.13:", type="build", when="@2.17.0:")

    depends_on("node-js@16:", type="build", when="@2.31.0:")
    depends_on("node-js@11.10.1:", type="build")

    depends_on("npm@7:", type="build", when="@2.31.0:")
    depends_on("npm", type="build", when="@2.30.0:")
    depends_on("yarn@1", type="build", when="@:2.29.2")

    def build(self, spec, prefix):
        make("build", parallel=False)

    def install(self, spec, prefix):
        mkdirp(prefix.bin)
        install("prometheus", prefix.bin)
        install("promtool", prefix.bin)
        if spec.satisfies("@:2.19.2"):
            install("tsdb/tsdb", prefix.bin)
        install_tree("documentation", prefix.documentation)
