# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyAbcpy(PythonPackage):
    """
    ABCpy is a highly modular, scientific library for approximate Bayesian
    computation (ABC) written in Python. It is designed to run all included ABC
    algorithms in parallel, either using multiple cores of a single computer or
    using an Apache Spark or MPI enabled cluster.
    """

    homepage = "https://github.com/eth-cscs/abcpy"
    pypi = "abcpy/abcpy-0.6.3.tar.gz"

    license("BSD-3-Clause-Clear")

    version(
        "0.6.3",
        sha256="b1c6e35d50daae1415085e4380fb643b8af3004ee493b90dd0c27786d9b08095",
        url="https://pypi.org/packages/af/7e/633fb84eac95a77c6a2e9302e5801da7d87e82014526427345aed5052ec6/abcpy-0.6.3-py3-none-any.whl",
    )

    with default_args(type="run"):
        depends_on("py-cloudpickle", when="@0.5.6:")
        depends_on("py-coverage", when="@0.2.2:")
        depends_on("py-glmnet@2.2.1:", when="@0.6:")
        depends_on("py-matplotlib", when="@0.5.7:")
        depends_on("py-mpi4py", when="@0.5.6:")
        depends_on("py-pot", when="@0.6:")
        depends_on("py-scikit-learn@0.23.1:", when="@0.6:")
        depends_on("py-scipy", when="@0.2.2:")
        depends_on("py-sklearn", when="@0.2.2:")
        depends_on("py-sphinx", when="@0.5.3:")
        depends_on("py-sphinx-rtd-theme", when="@0.2.2:")
        depends_on("py-tqdm", when="@0.5.7:")

    # Development dependencies are required in setup.py :(
