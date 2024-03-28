# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyPyaestro(PythonPackage):
    """A collection of data classes, data structures, and other utility classes
    that are aimed for use in workflow"""

    homepage = "https://github.com/FrankD412/pyaestro"
    pypi = "pyaestro/pyaestro-0.0.1a2.tar.gz"
    git = "https://github.com/FrankD412/pyaestro"

    maintainers("FrankD412")

    license("MIT")

    # git branches
    version(
        "0.0.1-alpha2",
        sha256="878504ba92ebd530c2c1ad40b1410d7ddd5f5c1e666ad12119e879d757c51f98",
        url="https://pypi.org/packages/60/df/91fa1e2b0f7bbf9b02e5d907421a476d7aad8ee1cd1c6253098833b782e6/pyaestro-0.0.1a2-py3-none-any.whl",
    )

    with default_args(type="run"):
        depends_on("py-coloredlogs")
        depends_on("py-psutil")
