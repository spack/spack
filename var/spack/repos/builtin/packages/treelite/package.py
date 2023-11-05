# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Treelite(CMakePackage):
    """Treelite is a model compiler for efficient deployment of
    decision tree ensembles."""

    homepage = "https://github.com/dmlc/treelite"
    url = "https://github.com/dmlc/treelite/archive/0.93.tar.gz"

    version("0.93", sha256="7d347372f7fdc069904afe93e69ed0bf696ba42d271fe2f8bf6835d2ab2f45d5")

    variant("protobuf", default=False, description="Build with protobuf")
    variant("python", default=True, description="Build with python support")

    depends_on("protobuf", when="+protobuf")
    depends_on("python@3.6:", type=("build", "run"), when="+python")
    depends_on("py-pip", type="build", when="+python")
    depends_on("py-wheel", type="build", when="+python")
    depends_on("py-setuptools", type="build", when="+python")
    depends_on("py-numpy", type=("build", "run"), when="+python")
    depends_on("py-scipy", type=("build", "run"), when="+python")

    build_directory = "build"

    def cmake_args(self):
        args = []

        if "+protobuf" in self.spec:
            args.append("-DENABLE_PROTOBUF:BOOL=ON")
            args.append("-DProtobuf_LIBRARY={0}".format(self.spec["protobuf"].prefix))
        else:
            args.append("-DENABLE_PROTOBUF:BOOL=OFF")

        return args

    @run_after("install")
    def python_install(self):
        if "+python" in self.spec:
            with working_dir("python"):
                args = std_pip_args + ["--prefix=" + self.prefix, "."]
                pip(*args)
