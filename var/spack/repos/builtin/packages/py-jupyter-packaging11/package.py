# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyJupyterPackaging11(PythonPackage):
    """Jupyter Packaging Utilities, version 11."""

    # TODO: This package only exists because different packages in the Jupyter ecosystem
    # require different versions of jupyter_packaging. Once the concretizer is capable
    # of concretizing build dependencies separately, this package should be removed.

    homepage = "https://github.com/jupyter/jupyter-packaging"
    pypi = "jupyter_packaging/jupyter_packaging-0.11.1.tar.gz"

    version("0.12.3", sha256="9d9b2b63b97ffd67a8bc5391c32a421bc415b264a32c99e4d8d8dd31daae9cf4")
    version("0.12.0", sha256="b27455d60adc93a7baa2e0b8f386be81b932bb4e3c0116046df9ed230cd3faac")
    version("0.11.1", sha256="6f5c7eeea98f7f3c8fb41d565a94bf59791768a93f93148b3c2dfb7ebade8eec")

    depends_on("python@3.7:", type=("build", "run"))
    depends_on("py-packaging", type=("build", "run"))
    depends_on("py-tomlkit", type=("build", "run"))
    depends_on("py-hatchling@0.25:", when="@0.12.3:", type="build")
    depends_on("py-setuptools@60.2:", when="@0.12:", type=("build", "run"))
    depends_on("py-setuptools@46.4:", type=("build", "run"))
    # https://github.com/jupyter/jupyter-packaging/issues/130
    depends_on("py-setuptools@:60", when="@:0.11", type=("build", "run"))
    depends_on("py-wheel", type=("build", "run"))
    depends_on("py-deprecation", type=("build", "run"))
