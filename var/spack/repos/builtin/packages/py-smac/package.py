# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PySmac(PythonPackage):
    """SMAC is a tool for algorithm configuration to optimize
    the parameters of arbitrary algorithms, including
    hyperparameter optimization of Machine Learning
    algorithms."""

    homepage = "https://automl.github.io/SMAC3/master/"
    pypi = "smac/smac-1.1.1.tar.gz"

    license("BSD-3-Clause")

    version(
        "1.1.1",
        sha256="c355dbb1992dc7ede0c310b9679b76835f7bfe66132c98e306774f812f3f5011",
        url="https://pypi.org/packages/ae/e1/33ec4c188aa54624abd17fe41bd1bf18342bc595da5425789b5c427b1913/smac-1.1.1-py3-none-any.whl",
    )

    with default_args(type="run"):
        depends_on("python@3.7:", when="@0.14:1.2,1.3.1:1")
        depends_on("py-configspace@0.4.14:0.4", when="@0.14:1.1")
        depends_on("py-dask", when="@0.14:1.1")
        depends_on("py-distributed", when="@0.14:1.1")
        depends_on("py-emcee@3.0.0:", when="@1.1.1:1.1")
        depends_on("py-joblib", when="@0.14:1.1")
        depends_on("py-numpy@1.7.1:", when="@0.14:1.1")
        depends_on("py-psutil", when="@0.14:1.1")
        depends_on("py-pynisher@0.4.1:", when="@0.14:1.1")
        depends_on("py-pyrfr@0.8:", when="@0.14:1.1")
        depends_on("py-scikit-learn@0.22:", when="@0.14:1.1")
        depends_on("py-scipy@1.7.0:", when="@0.14:1.1")
