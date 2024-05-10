# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyHail(PythonPackage):
    """Cloud-native genomic dataframes and batch computing (Python API)"""

    homepage = "https://hail.is"
    pypi = "hail/hail-0.2.130-py3-none-any.whl"

    maintainers("teaguesterling")
    license("MIT", checked_by="teaguesterling")

    version(
        "0.2.130", 
        sha256="c0f1f3ae52406a13eecb44ebe445be7d677d2c3b4e4e29269ecb53b7ac55168e", 
        expand=False
    )
    
    depends_on("python@3.9:", type=("build", "run"))
    depends_on("py-pip", type="build")
    depends_on("py-wheel", type="build")
    depends_on("py-avro@1.10:1.11", type=("build", "run"))
    depends_on("py-bokeh@:3.3", type=("build", "run"))
    depends_on("py-decorator@:4.4.2", type=("build", "run"))
    depends_on("py-deprecated@1.2.10:1.2", type=("build", "run"))
    depends_on("py-numpy@:2", type=("build", "run"))
    depends_on("py-pandas@2", type=("build", "run"))
    depends_on("py-parsimonious@:0", type=("build", "run"))
    depends_on("py-plotly@5.18:5.20", type=("build", "run"))
    depends_on("py-protobuf@3.20.2", type=("build", "run"))
    depends_on("py-pyspark@3.5", type=("build", "run"))
    depends_on("py-requests@2.31", type=("build", "run"))
    depends_on("py-scipy@1.3:1.11", type=("build", "run"))

    def setup_run_environment(self, env):
        #TODO: Add Spark configuration values to find HAIL Jars
        pass
