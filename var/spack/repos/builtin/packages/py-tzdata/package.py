# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyTzdata(PythonPackage):
    """Provider of IANA time zone data."""

    homepage = "https://github.com/python/tzdata"
    pypi = "tzdata/tzdata-2023.3.tar.gz"

    license("Apache-2.0")

    version(
        "2023.3",
        sha256="7e65763eef3120314099b6939b5546db7adce1e7d6f2e179e3df563c70511eda",
        url="https://pypi.org/packages/d5/fb/a79efcab32b8a1f1ddca7f35109a50e4a80d42ac1c9187ab46522b2407d7/tzdata-2023.3-py2.py3-none-any.whl",
    )
