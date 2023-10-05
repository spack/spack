# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class Bzip2(Package):
    """This is a thing"""

    homepage = "https://someplace.com"
    url = "https://anotherplace.com"

    version("1.0.8", sha256="ab5a03176ee106d3f0fa90e381da478ddae405918153cca248e682cd0c4a2269")

    variant("shared", default=True, description="Enables the build of shared libraries.")
