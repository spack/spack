# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class PyOptuna(PythonPackage):
    """Optuna is an automatic hyperparameter optimization software framework,
    particularly designed for machine learning. It features an imperative,
    define-by-run style user API. Thanks to our define-by-run API, the code
    written with Optuna enjoys high modularity, and the user of Optuna can
    dynamically construct the search spaces for the hyperparameters."""

    homepage = "https://optuna.org/"
    pypi = "optuna/optuna-3.2.0.tar.gz"

    maintainers("elliottslaughter", "eugeneswalker")

    license("MIT")

    version(
        "3.2.0",
        sha256="6140ca7cc1cc6751b5184c9f88cd7bbaaf6172b4bed1792552db9d8931979d77",
        url="https://pypi.org/packages/a0/8c/f72c6bc61b3c71149af95cd91e16149ea5b5aeae99e6d197f80e79a1035a/optuna-3.2.0-py3-none-any.whl",
    )

    with default_args(type="run"):
        depends_on("python@3.7:", when="@3.1:")
        depends_on("py-alembic@1.5:", when="@3.0.2:")
        depends_on("py-cmaes@0.9.1:", when="@3.1.0:3.2")
        depends_on("py-colorlog")
        depends_on("py-numpy")
        depends_on("py-packaging@20:")
        depends_on("py-pyyaml")
        depends_on("py-sqlalchemy@1.3.0:", when="@3.0.2:")
        depends_on("py-tqdm")
