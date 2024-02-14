# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class PyZfit(PythonPackage):
    """
    scalable pythonic model fitting for high energy physics
    """

    homepage = "https://github.com/zfit/zfit"
    pypi = "zfit/zfit-0.18.0.tar.gz"

    maintainers("jonas-eschle")
    license("BSD-3-Clause", checked_by="jonas-eschle")

    version("0.18.0", sha256="21d9479480f74945c67707b715780693bd4e94062c551bf41fe04a2eddb47fab")
    version("0.17.0", sha256="cd60dfc360c82666af4e8dddd78edb0ab95a095b9dd0868457f0981dc03afa5a")
    version("0.16.0", sha256="b3b170af23b61d7e265d6fb1bab1d052003f3fb41b3c537527cc1e5a1066dc10")
    version("0.15.5", sha256="00a1138429e8a7f830c9e229b9c0bcd6071b95dadd8c87eb81191079fb679225")
    version("0.14.1", sha256="66d1e349403f1d6c6350138d0f2b422046bcbdfb34fd95453dadae29a8b0c98a")

    depends_on("python@3.9:", type=("build", "run"))
    depends_on("py-setuptools", type="build")

    depends_on("py-tensorflow@2.15", type=("run"), when="@0.18")
    depends_on("py-tensorflow-probability@0.23", type=("run"), when="@0.18")

    depends_on("py-tensorflow@2.13", type=("run"), when="@0.15:0.17")
    depends_on("py-tensorflow-probability@0.21", type=("run"), when="@0.15:0.17")

    depends_on("py-tensorflow@2.12:2.13", type=("run"), when="@0.15:0.16")
    depends_on("py-tensorflow-probability@0.20:0.21", type=("run"), when="@0.15:0.16")

    depends_on("py-tensorflow@2.0:2.12", type=("run"), when="@0.14")
    depends_on("py-tensorflow-probability@0.20", type=("run"), when="@0.14")

    depends_on("py-boost-histogram", type=("run"))
    depends_on("py-colorama", type=("run"))
    depends_on("py-colored", type=("run"))
    depends_on("py-colorlog", type=("run"))
    depends_on("py-deprecated", type=("run"))
    depends_on("py-dill", type=("run"))
    depends_on("py-dotmap", type=("run"))
    depends_on("py-frozendict", type=("run"))
    depends_on("py-hist", type=("run"))
    depends_on("py-iminuit@2.3:", type=("run"))
    depends_on("py-jacobi", type=("run"))
    depends_on("py-numdifftools", type=("run"))
    depends_on("py-numpy@1.16:", type=("run"))
    depends_on("py-ordered-set", type=("run"))
    depends_on("py-pandas", type=("run"))
    depends_on("py-pydantic@1", type=("run"))
    depends_on("py-pyyaml", type=("run"))
    depends_on("py-scipy@1.2:", type=("run"))
    depends_on("py-tabulate", type=("run"))
    depends_on("py-texttable", type=("run"))
    depends_on("py-uhi", type=("run"))
    depends_on("py-uproot@4:", type=("run"))
    depends_on("py-xxhash", type=("run"))
    depends_on("py-zfit-interface", type=("run"))
