# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyDictdiffer(PythonPackage):
    """Dictdiffer is a helper module that helps you to diff and patch dictionares."""

    homepage = "https://github.com/inveniosoftware/dictdiffer"
    pypi = "dictdiffer/dictdiffer-0.8.1.tar.gz"

    version(
        "0.9.0",
        sha256="442bfc693cfcadaf46674575d2eba1c53b42f5e404218ca2c2ff549f2df56595",
        url="https://pypi.org/packages/47/ef/4cb333825d10317a36a1154341ba37e6e9c087bac99c1990ef07ffdb376f/dictdiffer-0.9.0-py2.py3-none-any.whl",
    )
    version(
        "0.8.1",
        sha256="d79d9a39e459fe33497c858470ca0d2e93cb96621751de06d631856adfd9c390",
        url="https://pypi.org/packages/97/92/350b6b6ec39c5f87d98d04c91a50c498518716a05368e6dea88b5c69b590/dictdiffer-0.8.1-py2.py3-none-any.whl",
    )
