# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyPyspark(PythonPackage):
    """Python bindings for Apache Spark"""

    homepage = "https://spark.apache.org"
    pypi = "pyspark/pyspark-3.0.1.tar.gz"

    version("3.3.1", sha256="e99fa7de92be406884bfd831c32b9306a3a99de44cfc39a2eefb6ed07445d5fa")
    version("3.3.0", sha256="7ebe8e9505647b4d124d5a82fca60dfd3891021cf8ad6c5ec88777eeece92cf7")
    version("3.2.1", sha256="0b81359262ec6e9ac78c353344e7de026027d140c6def949ff0d80ab70f89a54")
    version("3.1.3", sha256="39ac641ef5559a3d1286154779fc990316e9934520853615ae4785c1af52d14b")
    version("3.1.2", sha256="5e25ebb18756e9715f4d26848cc7e558035025da74b4fc325a0ebc05ff538e65")
    version("3.0.1", sha256="38b485d3634a86c9a2923c39c8f08f003fdd0e0a3d7f07114b2fb4392ce60479")
    version("2.4.4", sha256="13655eb113b8cf5f3f85b24fd92f86c4668a723723bd68949d028fa0df2cf694")
    version("2.3.2", sha256="7fb3b4fe47edb0fb78cecec37e0f2a728590f17ef6a49eae55141a7a374c07c8")
    version("2.3.0", sha256="0b3536910e154c36a94239f0ba0a201f476aadc72006409e5787198ffd01986e")

    depends_on("python@3.7:", when="@3.3.0:", type=("build", "run"))
    depends_on("python@3.6:", when="@3:3.2.3", type=("build", "run"))
    depends_on("python@2.7:3.7", when="@:2", type=("build", "run"))
    depends_on("python@2.7:", type=("build", "run"))
    depends_on("py-setuptools", type="build")
    depends_on("py-py4j@0.10.9.5", when="@3.3.0:", type=("build", "run"))
    depends_on("py-py4j@0.10.9.3", when="@3.2.1", type=("build", "run"))
    depends_on("py-py4j@0.10.9", when="@3.0.1:3.1.3", type=("build", "run"))
    depends_on("py-py4j@0.10.7", when="@2.3.2:2.4.4", type=("build", "run"))
    depends_on("py-py4j@0.10.6", when="@2.3.0", type=("build", "run"))

    def setup_run_environment(self, env):
        env.set("PYSPARK_PYTHON", self.spec["python"].command.path)
        env.set("PYSPARK_DRIVER_PYTHON", self.spec["python"].command.path)
