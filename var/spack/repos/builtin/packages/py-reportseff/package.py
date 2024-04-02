# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyReportseff(PythonPackage):
    """A python script for tabular display of slurm efficiency information."""

    homepage = "https://github.com/troycomi/reportseff"
    pypi = "reportseff/reportseff-2.7.2.tar.gz"

    license("MIT")

    version(
        "2.7.2",
        sha256="cbd355848982959dfbede6286f4e12f5cf8e309dd293526a238250398015df32",
        url="https://pypi.org/packages/98/d2/f7581f9cfa3c090ba2ddfb655b00170e8dcedc9c65372adeba2aff5a6fec/reportseff-2.7.2-py3-none-any.whl",
    )

    with default_args(type="run"):
        depends_on("python@3.7:3", when="@2.4:")
        depends_on("py-click@6.7:6.7.0,7:")
        depends_on("py-importlib-metadata@4.8.2:4", when="^python@:3.7")
