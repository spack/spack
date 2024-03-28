# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyDistributed(PythonPackage):
    """Distributed scheduler for Dask"""

    homepage = "https://distributed.dask.org/"
    pypi = "distributed/distributed-2.10.0.tar.gz"

    # 'distributed.dashboard.components' requires 'bokeh', but 'bokeh' is not listed as
    # a dependency. Leave out of 'import_modules' list to avoid unnecessary dependency.
    import_modules = [
        "distributed",
        "distributed.deploy",
        "distributed.comm",
        "distributed.comm.tests",
        "distributed.protocol",
        "distributed.cli",
        "distributed.dashboard",
        "distributed.http",
        "distributed.http.tests",
        "distributed.http.scheduler",
        "distributed.http.scheduler.prometheus",
        "distributed.http.worker",
        "distributed.diagnostics",
    ]

    license("BSD-3-Clause")

    version(
        "2023.4.1",
        sha256="14f9b106f069e528711190eb5fd871de48de2d023a97d63c146c2c4b80790ec8",
        url="https://pypi.org/packages/dd/26/7c3c4b2c7fc73028b989bf4c8d364e383a92403576aa417b523d7da91a18/distributed-2023.4.1-py3-none-any.whl",
    )
    version(
        "2022.10.2",
        sha256="ae4fffdb55c6cb510ba1cbdf2856563af80ebf93e5ceacb91c1ce79e7da108d8",
        url="https://pypi.org/packages/28/54/62702b9c98df725de6c7e88dd67c240f078cd657b1a3938a81bd1d977489/distributed-2022.10.2-py3-none-any.whl",
    )
    version(
        "2022.2.1",
        sha256="51ee30d5f55c968c7dfdb3054a31cb03fea7b9b012d9c4d498e3d813c7935099",
        url="https://pypi.org/packages/38/7a/8c2576048e36ec93d115af8d01bc10d936e5354c80f6b85bf25e11f85119/distributed-2022.2.1-py3-none-any.whl",
    )
    version(
        "2021.6.2",
        sha256="68251734ec68254280d855db5a77cead2712df2580ec9d44fde14321e7f3806c",
        url="https://pypi.org/packages/14/03/104c2cb8f498165da0037fbe76581678027ea2722bac2775f04aaeafef65/distributed-2021.6.2-py3-none-any.whl",
    )
    version(
        "2021.4.1",
        sha256="fe0e005e9aa79d68e185008bd2ce6562388311efd1c59a04ab6127ee631b8808",
        url="https://pypi.org/packages/63/f8/ac2c18adde6477bca3881c4d3cfa74c7f4da7ee82f3c83c201aa3b9ca5ee/distributed-2021.4.1-py3-none-any.whl",
    )
    version(
        "2020.12.0",
        sha256="532294b005009ce7c480073e467f9043c5292a735ed535f3fd00517a83a51bfc",
        url="https://pypi.org/packages/b5/12/3c25bb53c9b508e6332b62c33a8806ec7a33c926d8e32e7e53df0b512b84/distributed-2020.12.0-py3-none-any.whl",
    )

    with default_args(type="run"):
        depends_on("python@3.9:", when="@2023.5.1:")
        depends_on("py-click@8.0.0:", when="@2023.3.1:")
        depends_on("py-click@6.6:", when="@1.13.3:2022.10")
        depends_on("py-cloudpickle@1.5:", when="@2.21:")
        depends_on("py-dask@2023.4.1:2023.4", when="@2023.4.1:2023.4")
        depends_on("py-dask@2022.10.2:2022.10", when="@2022.10.2:2022.10")
        depends_on("py-dask@2022.2.1:2022.2", when="@2022.2.1:2022.2")
        depends_on("py-dask@2021.6.2:2021.6", when="@2021.6.2:2021.6")
        depends_on("py-dask@2021.3:", when="@2021.3:2021.4")
        depends_on("py-dask@2020:", when="@2020:2021.1")
        depends_on("py-jinja2@2.10.3:", when="@2023:")
        depends_on("py-jinja2", when="@2021.8:2022")
        depends_on("py-locket@1:", when="@2022.4.2:")
        depends_on("py-msgpack@1.0.0:", when="@2023:")
        depends_on("py-msgpack@0.6:", when="@2.11:2022")
        depends_on("py-packaging@20:", when="@2022:")
        depends_on("py-psutil@5.7:", when="@2023:2023.5.0")
        depends_on("py-psutil@5:", when="@1.24.1:2022")
        depends_on("py-pyyaml@5.3.1:", when="@2023:")
        depends_on("py-pyyaml", when="@1.22:2022")
        depends_on("py-setuptools", when="@2.9.1:2022.2")
        depends_on("py-sortedcontainers@2.0.5:", when="@2023:")
        depends_on("py-sortedcontainers@:1,2.0.2:", when="@1.22:2022")
        depends_on("py-tblib@1.6:", when="@2.11:")
        depends_on("py-toolz@0.10:", when="@2022.11.1:")
        depends_on("py-toolz@0.8.2:", when="@2.13:2022.11.0")
        depends_on("py-tornado@6.0.3:6.1", when="@2022.7:2022.11")
        depends_on("py-tornado@6.0.3:", when="@2.11:2022.6,2022.12:2023.5.0")
        depends_on("py-urllib3@1.24.3:", when="@2023:")
        depends_on("py-urllib3", when="@2022.4:2022")
        depends_on("py-zict@2.2:", when="@2023.4:2023.8")
        depends_on("py-zict@0.1.3:", when="@1.19:2022")

    # In Spack py-dask+distributed depends on py-distributed, not the other way around.
    # Hence, no need for depends_on("py-dask", ...)
    # Note that the setup.py is wrong for py-toolz, when="@2022.10.2".
    # See https://github.com/dask/distributed/pull/7309

    def patch(self):
        if self.spec.satisfies("@:2023.3"):
            filter_file("^dask .*", "", "requirements.txt")
