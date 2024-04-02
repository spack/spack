# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PySierrapy(PythonPackage):
    """A Client of HIVdb Sierra GraphQL Webservice"""

    homepage = "https://github.com/hivdb/sierra-client/tree/master/python"
    pypi = "sierrapy/sierrapy-0.3.0.tar.gz"

    maintainers("dorton21")

    version(
        "0.3.0",
        sha256="1c4d51a8c82384b68535735a4dfd5c847366f666ec9b76cea4be05763d2b03e4",
        url="https://pypi.org/packages/64/5c/87a5421a2d64b0f38dbcf404ad83a7602f153cbcd24fec3d863d41fe1a56/sierrapy-0.3.0-py2.py3-none-any.whl",
    )
