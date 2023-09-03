# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyObspy(PythonPackage):
    """ObsPy - a Python framework for seismological observatories."""

    homepage = "https://pypi.org/project/obspy/"
    pypi = "obspy/obspy-1.4.0.tar.gz"

    maintainers("francislz")

    version("1.4.0", sha256="336a6e1d9a485732b08173cb5dc1dd720a8e53f3b54c180a62bb8ceaa5fe5c06")
    version("1.2.1", sha256="340905ecc6d6d29dfc7103808e74e23e1fcfcbbc6ac32d07accce9a8b0322f47")

    depends_on("py-setuptools", type="build")
