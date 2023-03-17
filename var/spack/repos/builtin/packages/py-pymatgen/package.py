# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyPymatgen(PythonPackage):
    """Python Materials Genomics is a robust materials analysis code that
    defines core object representations for structures and molecules with
    support for many electronic structure codes. It is currently the core
    analysis code powering the Materials Project."""

    homepage = "http://www.pymatgen.org/"
    pypi = "pymatgen/pymatgen-2023.3.10.tar.gz"

    version("2022.8.23", sha256="e61c3eed297dc4865c21b0da95aea0fc76e78bd0ead3d2533494aefc05acb303")
    version("2021.3.9", sha256="a6f22d69133a48b7801bfd5e6a2878b47b4b4b2ef1a377b87c6c573be14cbf16")
    version(
        "2020.12.31", sha256="5002490facd47c55d2dae42c35712e061c1f5d881180485c0543a899589856d6"
    )

    extends("python@3.7:", ignore="bin/tabulate")

    # pymatgen does not support new recent python versions automatically.
    # Update below when support for 3.12 arrives in newer versions:
    conflicts("python@3.12:")
    # See https://pymatgen.org/change_log.html for python version support:
    conflicts("python@3.11:", when="@:2023.2.22")
    # pymatgen@:2022.1.8 does not support python@3.10:
    conflicts("python@3.10:", when="@:2022.1.08")
    # This conflict only applies to older, not checksummed versions:
    conflicts("python@3.9:", when="@:2020.10.9")

    depends_on("py-cython@0.29.23:", type="build", when="@2022.1.08:")
    depends_on("py-setuptools@43:", when="@2023:", type="build")
    depends_on("py-setuptools@18.0:", type="build")

    depends_on("py-numpy@1.9:", type=("build", "run"))
    depends_on("py-requests", type=("build", "run"))
    depends_on("py-monty@0.9.6:", type=("build", "run"))
    depends_on("py-scipy@0.14:", type=("build", "run"))
    depends_on("py-tabulate", type=("build", "run"))
    depends_on("py-spglib@1.9.8.7:", type=("build", "run"))
    depends_on("py-matplotlib@1.5:", type=("build", "run"))
    depends_on("py-palettable@2.1.1:", type=("build", "run"))

    # dependencies of never versions
    depends_on("py-matplotlib@1.5:", when="@2021.1.1:", type=("build", "run"))
    depends_on("py-monty@3.0.2:", when="@2021.1.1:", type=("build", "run"))
    # Enable once py-mp-api is packaged. Then, newer versions can be added:
    # depends_on("py-mp-api@0.27.3:", when="@2022.9:", type=("build", "run"))
    depends_on("py-networkx@2.2:", when="@2021.1.1:", type=("build", "run"))
    depends_on("py-numpy@1.20.1:", when="@2021.1.1:", type=("build", "run"))
    depends_on("py-palettable@3.1.1:", when="@2021.1.1:", type=("build", "run"))
    depends_on("py-pandas", when="@2021.1.1:", type=("build", "run"))
    depends_on("py-plotly@4.5.0:", when="@2021.1.1:", type=("build", "run"))
    depends_on("py-pybtex", when="@2022:", type=("build", "run"))
    depends_on("py-ruamel-yaml@0.15.6:", when="@2021.1.1:", type=("build", "run"))
    depends_on("py-ruamel-yaml@0.17.0:", when="@2022:", type=("build", "run"))
    depends_on("py-scipy@1.5.0:", when="@2021.1.1:", type=("build", "run"))
    depends_on("py-spglib@1.9.9.44:", when="@2021.1.1:", type=("build", "run"))
    depends_on("py-spglib@2.0.2:", when="@2022.10.22:", type=("build", "run"))
    depends_on("py-sympy", when="@2021.1.1:", type=("build", "run"))
    depends_on("py-tabulate", when="@2022:", type=("build", "run"))
    depends_on("py-tqdm", when="@2022:", type=("build", "run"))
    depends_on("py-uncertainties@3.1.4:", when="@2021.1.1:", type=("build", "run"))
