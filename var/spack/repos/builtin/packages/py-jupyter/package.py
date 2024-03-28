# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyJupyter(PythonPackage):
    """Jupyter metapackage. Install all the Jupyter components in one go."""

    homepage = "https://jupyter.org/"
    pypi = "jupyter/jupyter-1.0.0.tar.gz"

    license("BSD-3-Clause")

    version(
        "1.0.0",
        sha256="5b290f93b98ffbc21c0c7e749f054b3267782166d72fa5e3ed1ed4eaf34a2b78",
        url="https://pypi.org/packages/83/df/0f5dd132200728a86190397e1ea87cd76244e42d39ec5e88efd25b2abd7e/jupyter-1.0.0-py2.py3-none-any.whl",
    )

    # pip silently replaces distutils with setuptools
