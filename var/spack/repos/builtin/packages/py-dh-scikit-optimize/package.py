# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyDhScikitOptimize(PythonPackage):
    """A Modified version of scikit-optimize a Sequential model-based
    optimization toolbox for DeepHyper.
    Scikit-Optimize, or skopt, is a simple and efficient library to
    minimize (very) expensive and noisy black-box functions. It implements
    several methods for sequential model-based optimization. skopt aims to
    be accessible and easy to use in many contexts.

    The library is built on top of NumPy, SciPy and Scikit-Learn."""

    maintainers("Kerilk")

    homepage = "https://github.com/deephyper/scikit-optimize"
    pypi = "dh-scikit-optimize/dh-scikit-optimize-0.9.0.tar.gz"

    license("BSD-3-Clause")

    version(
        "0.9.5",
        sha256="2921adb41f4efa9c104c38126aa2fd5d4213e0db4da76fa506525a44bf8849ab",
        url="https://pypi.org/packages/c6/f4/19a326dcc62f6387bb6c91e52aa838c7be7671e5fb4fce7c5f98303eda6c/dh_scikit_optimize-0.9.5-py2.py3-none-any.whl",
    )
    version(
        "0.9.4",
        sha256="fc19c8083493b571b644d8484ec40ba57e5ed12c53fd3dbec7f5a6fd1696c60b",
        url="https://pypi.org/packages/0b/1b/2b7cffd77709717d3bc8cc0b3bac5f33d4e8001a91cbeefbc5e1c63fafe9/dh_scikit_optimize-0.9.4-py2.py3-none-any.whl",
    )
    version(
        "0.9.3",
        sha256="b170c3912e12157e189d3fe0faea0e7394073f05365f84990714f2713ca20dc0",
        url="https://pypi.org/packages/05/a8/6076430342ad6afaa062851f4c084eb83d2886aad3fe36093246cea25625/dh_scikit_optimize-0.9.3-py2.py3-none-any.whl",
    )
    version(
        "0.9.2",
        sha256="14ee454b11aa59b963992df33a72f66f7cdfb5abe333fd05236e7308001ad6e8",
        url="https://pypi.org/packages/bd/8b/4060e9050e40f016ff07625764c8b97c10b340464a7145dae9e297e41375/dh_scikit_optimize-0.9.2-py2.py3-none-any.whl",
    )
    version(
        "0.9.1",
        sha256="ac881251f7c60d76ac6d80d0e193247c7137de43c34818c5b173cc32103bd4b1",
        url="https://pypi.org/packages/57/e4/315511ee029de75ea1f3de7f962897efdc3b533c7e36d6276886a9c1d9ec/dh_scikit_optimize-0.9.1-py2.py3-none-any.whl",
    )
    version(
        "0.9.0",
        sha256="d2608b97f23839aab6049a7314fcd9d93d6df6574a449f69623f40b2e278582c",
        url="https://pypi.org/packages/c1/14/4a7825d71aac5a313e94b426d0116a523bbcb966b79360761a849ea57e6f/dh_scikit_optimize-0.9.0-py2.py3-none-any.whl",
    )

    variant("plots", default=False, description="Build with plot support from py-matplotlib")

    with default_args(type="run"):
        depends_on("py-joblib@0.11:")
        depends_on("py-matplotlib@2.0.0:", when="+plots")
        depends_on("py-numpy@1.13.3:", when="@0.9:")
        depends_on("py-pandas", when="@0.9.1:")
        depends_on("py-pyaml@16:")
        depends_on("py-scikit-learn@0.20.0:", when="@0.9:")
        depends_on("py-scipy@0.19.1:", when="@0.9:")
