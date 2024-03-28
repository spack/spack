# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyPyscaf(PythonPackage):
    """pyScaf orders contigs from genome assemblies utilising several types of
    information"""

    pypi = "pyScaf/pyScaf-0.12a4.tar.gz"

    license("GPL-3.0-only")

    version(
        "0.12-alpha4",
        sha256="8df880c5c0560fa1d2f76b509f964ed14baa0ed884b46616f28be5da4d538dac",
        url="https://pypi.org/packages/29/e4/fdc8ffca0a993076d240bc95afcc26c73feaec6128dd3073d07aad3cbed9/pyScaf-0.12a4-py2-none-any.whl",
    )

    with default_args(type="run"):
        depends_on("py-fastaindex", when="@0.12-alpha4:")
