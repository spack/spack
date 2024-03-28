# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyDask(PythonPackage):
    """Dask is a flexible parallel computing library for analytics."""

    homepage = "https://github.com/dask/dask/"
    pypi = "dask/dask-1.1.0.tar.gz"

    maintainers("skosukhin")

    license("BSD-3-Clause")

    version(
        "2023.4.1",
        sha256="d541c0a228ef3afd0185e932e4f887d1c3f7e852f1b4c7c2c22f6455d17640de",
        url="https://pypi.org/packages/54/25/480b2ae325f9be4bc99cbc77da0b757e285dabbeba3b82d43baa231e605b/dask-2023.4.1-py3-none-any.whl",
    )
    version(
        "2022.10.2",
        sha256="928003a97b890a14c8a09a01f15320d261053bda530a8bf191d84f33db4a63b8",
        url="https://pypi.org/packages/98/f1/2d9dcd8dd04544a2f1c02ca321aef84e57a712ec27842370084875c12b2a/dask-2022.10.2-py3-none-any.whl",
    )
    version(
        "2021.6.2",
        sha256="1f18d0815154b938a529ac3081c8952998d709319e57bbc484b42f0094217d43",
        url="https://pypi.org/packages/02/36/5e18bf30a172efd676fb7d668cc14d2624c15a4417b6c047e1def79ee450/dask-2021.6.2-py3-none-any.whl",
    )
    version(
        "2021.4.1",
        sha256="344c342d699466c3f742019b7a33caf2472b751f38370b200ede7d2f354aa1e4",
        url="https://pypi.org/packages/c3/23/42159cdb5c9edac174296c9976e175742513883f0f7bc132cfc2a2480fab/dask-2021.4.1-py3-none-any.whl",
    )
    version(
        "2020.12.0",
        sha256="5741db6e2426c001cecd374cba3bba8fea16a2da081089376ebcad9f8cf32aca",
        url="https://pypi.org/packages/73/95/72275bf8edd695ba6db792f4f09088a0c1ebe6506cb9790ff90b90219016/dask-2020.12.0-py3-none-any.whl",
    )

    variant("array", default=False)
    variant("bag", default=False)
    variant("complete", default=False)
    variant("dataframe", default=False)
    variant("delayed", default=False)
    variant("diagnostics", default=False)
    variant("distributed", default=False)

    with default_args(type="run"):
        depends_on("python@3.9:", when="@2023.5.1:")
        depends_on(
            "py-bokeh@2.4.2:2.4.2.0,2.4.3-rc1:2",
            when="@2022.10.1:2022.10,2022.11.1:2023.3+diagnostics",
        )
        depends_on(
            "py-bokeh@2.4.2:2.4.2.0,2.4.3-rc1:2",
            when="@2022.10.1:2022.10,2022.11.1:2023.3+complete",
        )
        depends_on(
            "py-bokeh@2.4.2:2.4.2.0,2.4.3-rc1:",
            when="@2022.3:2022.10.0,2022.11:2022.11.0,2023.4:+diagnostics",
        )
        depends_on(
            "py-bokeh@2.4.2:2.4.2.0,2.4.3-rc1:",
            when="@2022.3:2022.10.0,2022.11:2022.11.0+complete",
        )
        depends_on("py-bokeh@1:2.0.0-rc2,2.0.1:", when="@2.26:2021.11+diagnostics")
        depends_on("py-bokeh@1:2.0.0-rc2,2.0.1:", when="@2.26:2021.11+complete")
        depends_on("py-click@8.0.0:", when="@2023.4.1:2023.10")
        depends_on("py-click@7:", when="@2022.10.1:2023.4.0")
        depends_on("py-cloudpickle@1.5:", when="@2023.4.1:")
        depends_on("py-cloudpickle@1.1:", when="@2021.3.1:2023.4.0")
        depends_on("py-cloudpickle@0.2.2:", when="@2.13:2021.3.0+delayed")
        depends_on("py-cloudpickle@0.2.2:", when="@2.13:2021.3.0+bag")
        depends_on("py-cloudpickle@0.2.2:", when="@2.13:2.17.0,2.17.2:2021.3.0+complete")
        depends_on("py-distributed@2023.4.1:2023.4", when="@2023.4.1:2023.4+distributed")
        depends_on("py-distributed@2022.10.2:2022.10", when="@2022.10.2:2022.10+distributed")
        depends_on("py-distributed@2022.10.2:2022.10", when="@2022.10.2:2022.10+complete")
        depends_on("py-distributed@2021.6.2:2021.6", when="@2021.6.2:2021.6+distributed")
        depends_on("py-distributed@2021.6.2:2021.6", when="@2021.6.2:2021.6+complete")
        depends_on("py-distributed@2021.4.1:", when="@2021.4.1:2021.4+distributed")
        depends_on("py-distributed@2021.4.1:", when="@2021.4.1:2021.4+complete")
        depends_on("py-distributed@2:", when="@2:2021.2+distributed")
        depends_on("py-distributed@2:", when="@2:2.17.0,2.17.2:2021.2+complete")
        depends_on("py-fsspec@2021.9:", when="@2023.4.1:")
        depends_on("py-fsspec@0.6:", when="@2021.3.1:2023.4.0")
        depends_on("py-fsspec@0.6:", when="@2.8:2021.3.0+dataframe")
        depends_on("py-fsspec@0.6:", when="@2.8:2021.3.0+bag")
        depends_on("py-fsspec@0.6:", when="@2.8:2.17.0,2.17.2:2021.3.0+complete")
        depends_on("py-importlib-metadata@4.13:", when="@2024.3: ^python@:3.11")
        depends_on("py-importlib-metadata@4.13:", when="@2023.3.2:2024.2")
        depends_on("py-jinja2@2.10.3:", when="@2023.3:+diagnostics")
        depends_on("py-jinja2@2.10.3:", when="@2023.3+complete")
        depends_on("py-jinja2", when="@2021.8.1:2023.2+diagnostics")
        depends_on("py-jinja2", when="@2021.8.1:2023.2+complete")
        depends_on("py-lz4@4.3.2:", when="@2023.3.1:+complete")
        depends_on("py-numpy@1.21.0:", when="@2023.2.1:+array")
        depends_on("py-numpy@1.21.0:", when="@2023.2.1:2023.7+dataframe")
        depends_on("py-numpy@1.21.0:", when="@2023.2.1:2023.3+complete")
        depends_on("py-numpy@1.18.0:", when="@2021.8:2023.2.0+dataframe")
        depends_on("py-numpy@1.18.0:", when="@2021.8:2023.2.0+complete")
        depends_on("py-numpy@1.18.0:", when="@2021.8:2023.2.0+array")
        depends_on("py-numpy@1.16.0:", when="@2021.3.1:2021.7+dataframe")
        depends_on("py-numpy@1.16.0:", when="@2021.3.1:2021.7+complete")
        depends_on("py-numpy@1.16.0:", when="@2021.3.1:2021.7+array")
        depends_on("py-numpy@1.15.1:", when="@2020:2021.3.0+dataframe")
        depends_on("py-numpy@1.15.1:", when="@2020:2021.3.0+complete")
        depends_on("py-numpy@1.15.1:", when="@2020:2021.3.0+array")
        depends_on("py-packaging@20:", when="@2021.7.1:")
        depends_on("py-pandas@1.3.0:", when="@2023.2.1:+dataframe")
        depends_on("py-pandas@1.3.0:", when="@2023.2.1:2023.3+complete")
        depends_on("py-pandas@1.0.0:", when="@2021.8:2023.2.0+dataframe")
        depends_on("py-pandas@1.0.0:", when="@2021.8:2023.2.0+complete")
        depends_on("py-pandas@0.25.0:", when="@2020:2021.7+dataframe")
        depends_on("py-pandas@0.25.0:", when="@2020:2021.7+complete")
        depends_on("py-partd@1.2:", when="@2023.2.1:")
        depends_on("py-partd@0.3.10:", when="@2021.3.1:2023.2.0")
        depends_on("py-partd@0.3.10:", when="@2:2021.3.0+dataframe")
        depends_on("py-partd@0.3.10:", when="@2:2021.3.0+bag")
        depends_on("py-partd@0.3.10:", when="@2:2.17.0,2.17.2:2021.3.0+complete")
        depends_on("py-pyarrow@7:", when="@2023.3.1:+complete")
        depends_on("py-pyyaml@5.3.1:", when="@2022:")
        depends_on("py-pyyaml", when="@2.17.1:2021")
        depends_on("py-pyyaml", when="@2.7:2.17.0+complete")
        depends_on("py-toolz@0.10:", when="@2023.4.1:")
        depends_on("py-toolz@0.8.2:", when="@2021.3.1:2023.4.0")
        depends_on("py-toolz@0.8.2:", when="@2.13:2021.3.0+delayed")
        depends_on("py-toolz@0.8.2:", when="@2.13:2021.3.0+dataframe")
        depends_on("py-toolz@0.8.2:", when="@2.13:2021.3.0+bag")
        depends_on("py-toolz@0.8.2:", when="@2.13:2021.3.0+array")
        depends_on("py-toolz@0.8.2:", when="@2.13:2.17.0,2.17.2:2021.3.0+complete")

        # self-dependency
        # depends_on("py-dask+array+dataframe+diagnostics+distributed", when="@2023.4:+complete")

    # Common requirements

    # Requirements for dask.array
    # The dependency on py-toolz is non-optional starting version 2021.3.1

    # Requirements for dask.bag
    # The dependency on py-cloudpickle is non-optional starting version 2021.3.1
    # The dependency on py-fsspec is non-optional starting version 2021.3.1
    # The dependency on py-toolz is non-optional starting version 2021.3.1
    # The dependency on py-partd is non-optional starting version 2021.3.1

    # Requirements for dask.dataframe
    # The dependency on py-toolz is non-optional starting version 2021.3.1
    # The dependency on py-partd is non-optional starting version 2021.3.1
    # The dependency on py-fsspec is non-optional starting version 2021.3.1

    # Requirements for dask.distributed

    # Requirements for dask.diagnostics

    # Requirements for dask.delayed
    # The dependency on py-cloudpickle is non-optional starting version 2021.3.1
    # The dependency on py-toolz is non-optional starting version 2021.3.1

    @property
    def import_modules(self):
        modules = ["dask", "dask.bytes"]

        if "+array" in self.spec:
            modules.append("dask.array")

        if "+bag" in self.spec:
            modules.append("dask.bag")

        if "+dataframe" in self.spec:
            modules.extend(["dask.dataframe", "dask.dataframe.tseries", "dask.dataframe.io"])

        if "+diagnostics" in self.spec:
            modules.append("dask.diagnostics")

        return modules
