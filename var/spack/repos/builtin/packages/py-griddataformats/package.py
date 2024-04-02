# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyGriddataformats(PythonPackage):
    """The gridDataFormats package provides classes to unify reading
    and writing n-dimensional datasets. One can read grid data from
    files, make them available as a Grid object, and write out the
    data again."""

    homepage = "http://www.mdanalysis.org/GridDataFormats"
    pypi = "GridDataFormats/GridDataFormats-0.5.0.tar.gz"

    maintainers("RMeli")

    license("LGPL-3.0-only")

    version(
        "1.0.1",
        sha256="c2c45c9ea18f29ffd8fe311d5322b4cba4f4e4c76980ec4e2e9a7f296b208a46",
        url="https://pypi.org/packages/03/f7/a676afdb039c77eb012f4cdbed231e44555cc90025ce660d17cbeecdc9f9/GridDataFormats-1.0.1-py3-none-any.whl",
    )

    with default_args(type="run"):
        depends_on("python@3.8:", when="@1.0.1")
        depends_on("py-mrcfile", when="@0.7:")
        depends_on("py-numpy@1.19.0:", when="@1:1.0.1")
        depends_on("py-scipy", when="@0.4.1:")
