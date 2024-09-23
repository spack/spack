# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

# ----------------------------------------------------------------------------
# If you submit this package back to Spack as a pull request,
# please first remove this boilerplate and all FIXME comments.
#
# This is a template package file for Spack.  We've put "FIXME"
# next to all the things you'll want to change. Once you've handled
# them, you can save this file and test your package like this:
#
#     spack install py-expandvars
#
# You can edit this file again by typing:
#
#     spack edit py-expandvars
#
# See the Spack documentation for more information on packaging.
# ----------------------------------------------------------------------------

from spack.package import *


class PyExpandvars(PythonPackage):
    """Expand system variables Unix style"""

    homepage = "https://github.com/sayanarijit/expandvars"
    pypi = "expandvars/expandvars-0.12.0.tar.gz"

    maintainers("Chrismarsh")

    license("MIT", checked_by="Chrismarsh")

    version("0.12.0", sha256="7d1adfa55728cf4b5d812ece3d087703faea953e0c0a1a78415de9df5024d844")

    # FIXME: Add dependencies if required.
    depends_on("py-hatchling")

