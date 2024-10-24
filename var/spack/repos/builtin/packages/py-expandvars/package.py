# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyExpandvars(PythonPackage):
    """Expand system variables Unix style"""

    homepage = "https://github.com/sayanarijit/expandvars"
    pypi = "expandvars/expandvars-0.12.0.tar.gz"

    maintainers("Chrismarsh")

    license("MIT", checked_by="Chrismarsh")

    version("0.12.0", sha256="7d1adfa55728cf4b5d812ece3d087703faea953e0c0a1a78415de9df5024d844")

    depends_on("py-hatchling")
