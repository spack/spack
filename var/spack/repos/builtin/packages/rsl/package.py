# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Rsl(AutotoolsPackage):
    """This library is an object oriented programming environment for writing
    software applicable to all RADAR data related to the TRMM GV effort."""

    homepage = "https://trmm-fc.gsfc.nasa.gov/trmm_gv/software/rsl/"
    url = "https://trmm-fc.gsfc.nasa.gov/trmm_gv/software/rsl/software/rsl-v1.50.tar.gz"

    version("1.50", sha256="9e4e3fe45eb1e4aebea63255d4956b00eb69527044a83f182cde1b43510bd342")

    depends_on("bzip2")
    depends_on("jpeg")
    depends_on("zlib")
