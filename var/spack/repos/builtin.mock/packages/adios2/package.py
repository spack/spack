# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class Adios2(Package):
    """The Adaptable Input Output System version 2,
    developed in the Exascale Computing Program"""

    homepage = "https://someplace.com"
    url = "https://anotherplace.com"

    version("2.9.1", sha256="ddfa32c14494250ee8a48ef1c97a1bf6442c15484bbbd4669228a0f90242f4f9")

    variant("shared", default=True, description="Build shared libraries")
    variant("bzip2", default=True, description="Enable BZip2 compression")

    depends_on("bzip2")
