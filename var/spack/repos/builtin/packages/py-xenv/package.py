# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyXenv(PythonPackage):
    """Helpers to work with the environment in a platform independent way."""

    homepage = "https://gitlab.cern.ch/gaudi/xenv"
    pypi = "xenv/xenv-1.0.0.tar.gz"
    git = "https://gitlab.cern.ch/gaudi/xenv.git"

    license("GPL-3.0-or-later")

    version(
        "1.0.0",
        sha256="e941ebbf479e03f4109d8c49cf4201f337418d221abbdea6ad9b7656e2bbc1ed",
        url="https://pypi.org/packages/1b/a8/6cfed952e22f2e7a711c71c43426e777fe6aaad50f6262b7e0617b17ba36/xenv-1.0.0-py2.py3-none-any.whl",
    )

    with default_args(type="run"):
        depends_on("python@:3", when="@:0.0.4,1:")
