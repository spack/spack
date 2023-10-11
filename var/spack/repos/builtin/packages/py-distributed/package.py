# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyDistributed(PythonPackage):
    """Distributed scheduler for Dask"""

    homepage = "https://distributed.dask.org/"
    pypi = "distributed/distributed-2.10.0.tar.gz"
    git = "https://github.com/dask/distributed.git"

    version("2023.9.3", sha256="1161efaf7aa520fd0653ec48ceb59d3bc7d8931be392cf8bc7b89079739243e5")
    version("2023.4.1", sha256="0140376338efdcf8db1d03f7c1fdbb5eab2a337b03e955d927c116824ee94ac5")
    version("2022.10.2", sha256="53f0a5bf6efab9a5ab3345cd913f6d3f3d4ea444ee2edbea331c7fef96fd67d0")
    version("2022.2.1", sha256="fb62a75af8ef33bbe1aa80a68c01a33a93c1cd5a332dd017ab44955bf7ecf65b")
    version("2021.6.2", sha256="d7d112a86ab049dcefa3b21fd1baea4212a2c03d22c24bd55ad38d21a7f5d148")
    version("2021.4.1", sha256="4c1b189ec5aeaf770c473f730f4a3660dc655601abd22899e8a0662303662168")
    version("2020.12.0", sha256="2a0b6acc921cd4e0143a7c4383cdcbed7defbc4bd9dc3aab0c7f1c45f14f80e1")

    depends_on("python@3.9:", when="@2023.5.1:", type=("build", "run"))
    depends_on("python@3.8:", when="@2022.2.1:", type=("build", "run"))
    depends_on("py-setuptools@62.6:", when="@2023.4.1:", type="build")
    depends_on("py-setuptools", type="build")
    depends_on("py-versioneer@0.28+toml", when="@2023.4.1:", type="build")

    depends_on("py-click@8:", when="@2023.4.1:", type=("build", "run"))
    depends_on("py-click@6.6:", type=("build", "run"))
    depends_on("py-cloudpickle@1.5:", type=("build", "run"))
    depends_on("py-dask@2023.9.3", when="@2023.9.3", type=("build", "run"))
    depends_on("py-dask@2023.4.1", when="@2023.4.1", type=("build", "run"))
    depends_on("py-jinja2@2.10.3:", when="@2023.4.1:", type=("build", "run"))
    depends_on("py-jinja2", when="@2022.2.1:", type=("build", "run"))
    depends_on("py-locket@1:", when="@2022.2.1:", type=("build", "run"))
    depends_on("py-msgpack@1:", when="@2023.4.1:", type=("build", "run"))
    depends_on("py-msgpack@0.6:", type=("build", "run"))
    depends_on("py-packaging@20:", when="@2022.2.1:", type=("build", "run"))
    depends_on("py-psutil@5.7.2:", when="@2023.5.1:", type=("build", "run"))
    depends_on("py-psutil@5.7:", when="@2023.4.1:", type=("build", "run"))
    depends_on("py-psutil@5:", type=("build", "run"))
    depends_on("py-pyyaml@5.3.1:", when="@2023.4.1:", type=("build", "run"))
    depends_on("py-pyyaml", type=("build", "run"))
    depends_on("py-sortedcontainers@2.0.5:", when="@2023.4.1:", type=("build", "run"))
    depends_on("py-sortedcontainers@:1,2.0.2:", type=("build", "run"))
    depends_on("py-tblib@1.6:", type=("build", "run"))
    # Note that the setup.py is wrong for py-toolz, when="@2022.10.2".
    # See https://github.com/dask/distributed/pull/7309
    depends_on("py-toolz@0.10:", when="@2022.10.2:", type=("build", "run"))
    depends_on("py-toolz@0.8.2:", type=("build", "run"))
    depends_on("py-tornado@6.0.4:", when="@2023.5.1:", type=("build", "run"))
    depends_on("py-tornado@6.0.3:", when="@2022.12:", type=("build", "run"))
    depends_on("py-tornado@6.0.3:6.1", when="@2022.10.2:2022.11.1", type=("build", "run"))
    depends_on("py-tornado@6.0.3:", when="^python@3.8:", type=("build", "run"))
    depends_on("py-tornado@5:", when="^python@:3.7", type=("build", "run"))
    depends_on("py-urllib3@1.24.3:", when="@2023.4.1:", type=("build", "run"))
    depends_on("py-urllib3", when="@2022.10.2:", type=("build", "run"))
    depends_on("py-zict@3:", when="@2023.9:", type=("build", "run"))
    depends_on("py-zict@2.2:", when="@2023.4.1:", type=("build", "run"))
    depends_on("py-zict@0.1.3:", type=("build", "run"))

    # 'distributed.dashboard.components' requires 'bokeh', but 'bokeh' is not listed as
    # a dependency. Leave out of 'import_modules' list to avoid unnecessary dependency.
    skip_modules = ["distributed.dashboard.components"]

    def patch(self):
        if self.spec.satisfies("@:2023.3"):
            filter_file("^dask .*", "", "requirements.txt")
