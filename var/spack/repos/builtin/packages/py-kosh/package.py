# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class PyKosh(PythonPackage):
    """
    Kosh allows codes to store, query, share data via an easy-to-use Python API.
    Kosh lies on top of Sina and can use any database backend supported by Sina.
    In adition Kosh aims to make data access and sharing as simple as possible.
    """

    homepage = "https://github.com/LLNL/kosh"
    url = "https://github.com/LLNL/kosh/archive/refs/tags/v2.0.tar.gz"

    # notify when the package is updated.
    maintainers("doutriaux1")

    license("MIT")

    version(
        "3.0.1",
        sha256="5592976045ddc06730ac02cb07f9e1b9f3a47d464cb81c4a172e62632420676a",
        url="https://pypi.org/packages/08/84/7b2915ea8b74918a54922148d9f4ec8293da813967408adc1e2f6471d6b0/kosh-3.0.1-py3-none-any.whl",
    )
    version(
        "2.2",
        sha256="0a82cfda7390ce4ea1b3cecd2acf591602a8c71886a93ed0c4a827e52e8edab3",
        url="https://pypi.org/packages/33/60/a9bb40ed3678d8cc08677626c2fdeeb70049d2e6e36e8fc6b5479e7a94a4/kosh-2.2-py3-none-any.whl",
    )
    version(
        "2.1",
        sha256="c5ae6c121f7669cff01fc58d49ee9a413ba78606d8877c31c7f61bc43ffac229",
        url="https://pypi.org/packages/85/f9/62fbdb9dd1710cebf64697686cd66a2e4c2294251042c3bab4a6538a58ed/kosh-2.1-py3-none-any.whl",
    )
    version(
        "2.0",
        sha256="7688f3da51b8fc9c154294071e435e0821423260b625c2ff7c1c1a31ccbb35e9",
        url="https://pypi.org/packages/b1/80/983b9fbc40caa1ac2a4f481e3b576849e7fceb9e304e77d5ac38b3795a0e/kosh-2.0-py3-none-any.whl",
    )

    with default_args(type="run"):
        depends_on("py-h5py@3.0.0:", when="@3:")
        depends_on("py-hdbscan", when="@3:")
        depends_on("py-llnl-sina@1.11:", when="@2:")
        depends_on("py-matplotlib", when="@3:")
        depends_on("py-networkx@2.6:", when="@3:")
        depends_on("py-networkx", when="@:0.0.0,1.1:2")
        depends_on("py-numpy@1.20.0:", when="@3:")
        depends_on("py-numpy", when="@:0.0.0,1.1:2")
        depends_on("py-pandas", when="@3:")
        depends_on("py-scikit-learn@1.0.2:", when="@3:")
        depends_on("py-scipy", when="@3:")
        depends_on("py-tqdm", when="@3:")
