# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyGeopandas(PythonPackage):
    """GeoPandas is an open source project to make working with geospatial
    data in python easier. GeoPandas extends the datatypes used by pandas
    to allow spatial operations on geometric types. Geometric operations are
    performed by shapely. Geopandas further depends on fiona for file access
    and descartes and matplotlib for plotting."""

    homepage = "https://geopandas.org/"
    pypi = "geopandas/geopandas-0.8.1.tar.gz"
    git = "https://github.com/geopandas/geopandas.git"

    maintainers("adamjstewart")

    license("BSD-3-Clause")

    version(
        "0.14.3",
        sha256="41b31ad39e21bc9e8c4254f78f8dc4ce3d33d144e22e630a00bb336c83160204",
        url="https://pypi.org/packages/90/37/08e416c9915dcf7d53deb0fbdb702266902c584617dfa6e6c84fb2fc6ee3/geopandas-0.14.3-py3-none-any.whl",
    )
    version(
        "0.11.1",
        sha256="f3344937f3866e52996c7e505d56dae78be117dc840cd1c23507da0b33c0af71",
        url="https://pypi.org/packages/de/83/08b7284066b268e71019398b9094b1c860816aa9b9422f1c489459bfbdf1/geopandas-0.11.1-py3-none-any.whl",
    )
    version(
        "0.11.0",
        sha256="0991f279d4f9e3a04e3666f32b1ac64d6ba439933da3d9654a26031e0ccea5dc",
        url="https://pypi.org/packages/50/81/d9e453085c3c7bf36f21f6766a23c2503de8f709fda5eb7c46b2caf10aa8/geopandas-0.11.0-py3-none-any.whl",
    )
    version(
        "0.10.2",
        sha256="1722853464441b603d9be3d35baf8bde43831424a891e82a8545eb8997b65d6c",
        url="https://pypi.org/packages/a6/92/5ddb9aab70fcca4b35e4b0b7ba1c1f994873cb13b139f4846a621bbcc936/geopandas-0.10.2-py2.py3-none-any.whl",
    )
    version(
        "0.10.1",
        sha256="9fce7062b5d2ca162d2b14c5a8d6f2a34a4158176214fafd683964df7444eb5e",
        url="https://pypi.org/packages/6e/ff/b337f60fc23802d41513c798e40782dd2c9b12e95ced90c987f66f0676e8/geopandas-0.10.1-py2.py3-none-any.whl",
    )
    version(
        "0.10.0",
        sha256="9fc4711e48f53982ccbc9821c936205657c46e3b9881c73efd4daec67d46f31a",
        url="https://pypi.org/packages/57/24/82715b629f58318c96881a536bf3ddd8638d3458d8b90bf63955fd949a63/geopandas-0.10.0-py2.py3-none-any.whl",
    )
    version(
        "0.9.0",
        sha256="79f6e557ba0dba76eec44f8351b1c6b42a17c38f5f08fef347e98fe4dae563c7",
        url="https://pypi.org/packages/d7/bf/e9cefb69d39155d122b6ddca53893b61535fa6ffdad70bf5ef708977f53f/geopandas-0.9.0-py2.py3-none-any.whl",
    )
    version(
        "0.8.2",
        sha256="8f53aa98e4ddb054afc46d289c930e96267d32c35c3dc685721ec2fddee77e60",
        url="https://pypi.org/packages/2a/9f/e8a440a993e024c0d3d4e5c7d3346367c50c9a1a3d735caf5ee3bde0aab1/geopandas-0.8.2-py2.py3-none-any.whl",
    )
    version(
        "0.8.1",
        sha256="ef90a7f5ce9337f412c1dab9e014b4076b639fb7fc0edcf8b57c252c91a096c4",
        url="https://pypi.org/packages/f7/a4/e66aafbefcbb717813bf3a355c8c4fc3ed04ea1dd7feb2920f2f4f868921/geopandas-0.8.1-py2.py3-none-any.whl",
    )
    version(
        "0.5.0",
        sha256="7261f76afefda02b6039015431cc727f6089fcdfdf69443cef4f31620f1efcac",
        url="https://pypi.org/packages/74/42/f4b147fc7920998a42046d0c2e65e61000bc5d104f1f8aec719612cb2fc8/geopandas-0.5.0-py2.py3-none-any.whl",
    )
    version(
        "0.4.0",
        sha256="1c272a9dfa1a382a153d6854d56be33b4c991670ebfdf05d562965877da5e9b8",
        url="https://pypi.org/packages/24/11/d77c157c16909bd77557d00798b05a5b6615ed60acb5900fbe6a65d35e93/geopandas-0.4.0-py2.py3-none-any.whl",
    )
    version(
        "0.3.0",
        sha256="38ec319ce8be344728cf124847251952af49adea8d38229723a55cc1ea473d44",
        url="https://pypi.org/packages/0a/0e/8ae74743ed7915ddb7d70cc8dfa8fc0b9b9cc81205c6e288a01915a46192/geopandas-0.3.0-py2.py3-none-any.whl",
    )

    with default_args(type="run"):
        depends_on("python@3.9:", when="@0.14:")
        depends_on("python@3.8:", when="@0.11:0.13")
        depends_on("python@3.7:", when="@0.10")
        depends_on("py-descartes", when="@0.2.1:0.3")
        depends_on("py-fiona@1.8.21:", when="@0.14:")
        depends_on("py-fiona@1.8.0:", when="@0.9:0.12")
        depends_on("py-fiona", when="@0.2.1:0.4,0.5.1:0.6.0-rc1,0.6.1:0.8")
        depends_on("py-packaging", when="@0.11:")
        depends_on("py-pandas@1.4.0:", when="@0.14:")
        depends_on("py-pandas@1.0.0:", when="@0.11:0.12")
        depends_on("py-pandas@0.25.0:", when="@0.10")
        depends_on("py-pandas@0.24.0:", when="@0.9")
        depends_on("py-pandas@0.23.0:", when="@0.6:0.6.0-rc1,0.6.1:0.8")
        depends_on("py-pandas", when="@0.2.1:0.4,0.5.1:0.5")
        depends_on("py-pyproj@3.3:", when="@0.14:")
        depends_on("py-pyproj@2.6.1.post:", when="@0.11:0.12")
        depends_on("py-pyproj@2.2:", when="@0.7:0.10")
        depends_on("py-pyproj", when="@0.2.1:0.4,0.5.1:0.6.0-rc1,0.6.1:0.6")
        depends_on("py-shapely@1.8.0:", when="@0.14:")
        depends_on("py-shapely@1.7.0:1", when="@0.11:0.12.0")
        depends_on("py-shapely@1.6.0:", when="@0.9:0.10")
        depends_on("py-shapely", when="@0.2.1:0.4,0.5.1:0.6.0-rc1,0.6.1:0.8")
