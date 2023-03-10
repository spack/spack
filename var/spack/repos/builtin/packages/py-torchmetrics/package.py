# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyTorchmetrics(PythonPackage):
    """Machine learning metrics for distributed, scalable PyTorch applications."""

    homepage = "https://github.com/PyTorchLightning/metrics"
    pypi = "torchmetrics/torchmetrics-0.3.1.tar.gz"

    maintainers("adamjstewart")

    version("0.11.3", sha256="6a2bcc17361f0e4c1668c92595b12ef30ccf9ef1d03263bee7c6136a882afe30")
    version("0.11.2", sha256="5a1f5fff9b1fb695bbcab6442d768e2e9b9535d00f4b4dea9ce03d40c866be07")
    version("0.11.1", sha256="de2e9feb3316f798ab08b318302ff04e764f47e691f0847f780044279fa176ca")
    version("0.11.0", sha256="c838e0491d80775daadd0802e27ae3af112a52086c9ba8cbcd1e2807243c89ac")
    version("0.10.3", sha256="9e6ab66175f2dc13e246c37485b2c27c77931dfe47fc2b81c76217b8efdc1e57")
    version("0.10.2", sha256="daa29d96bff5cff04d80eec5b9f5076993d6ac9c2d2163e88b6b31f8d38f7c25")
    version("0.10.1", sha256="e892ecd413e6bf63950329d1317c70f697d81d0f7e386152238062e322c8f1f3")
    version("0.10.0", sha256="990bafc7f76d7442894533771d0ba7492dbca2bbf2989fb32de7e9c68eb3d133")
    version("0.9.3", sha256="4ebfd2466021db26397636966ee1a195d3b340ba5d71bb258e764340dfc2476f")
    version("0.9.2", sha256="8178c9242e243318093d9b7237738a504535193d2006da6e58b0ed4003e318d2")
    version("0.9.0", sha256="3aa32ea575915b313d872d3460996c0f12a7bb37e6ce3da0e8d80865603b89f6")
    version("0.7.0", sha256="dbfb8989086f38020045a935e83928504e1af1d84ae92b073f6a83d018f4bc00")
    version("0.5.1", sha256="22fbcb6fc05348ca3f2bd06e0763e88411a6b68c2b9fc26084b39d40cc4021b0")
    version("0.4.1", sha256="2fc50f812210c33b8c2649dbb1482e3c47e93cae33e4b3d0427fb830384effbd")
    version("0.3.1", sha256="78f4057db53f7c219fdf9ec9eed151adad18dd43488a44e5c780806d218e3f1d")
    version("0.2.0", sha256="481a28759acd2d77cc088acba6bc7dc4a356c7cb767da2e1495e91e612e2d548")

    depends_on("py-setuptools", type="build")
    depends_on("py-numpy@1.17.2:", when="@0.4:", type=("build", "run"))
    depends_on("py-numpy", when="@0.3:", type=("build", "run"))
    depends_on("py-torch@1.8.1:", when="@0.11:", type=("build", "run"))
    depends_on("py-torch@1.3.1:", type=("build", "run"))
    depends_on("py-pydeprecate@0.3", when="@0.7:0.8", type=("build", "run"))
    depends_on("py-packaging", when="@0.3:", type=("build", "run"))
    depends_on("py-typing-extensions", when="@0.9: ^python@:3.8", type=("build", "run"))
