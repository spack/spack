# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Mct(AutotoolsPackage):
    """Model Coupling Toolkit (MCT): toolkit to support the construction
    of highly portable and extensible high-performance couplers for
    distributed memory parallel coupled models."""

    homepage = "https://github.com/MCSclimate/MCT"
    url = "https://github.com/MCSclimate/MCT/archive/refs/tags/MCT_2.11.0.tar.gz"

    maintainers("climbfuji")

    # This is a custom license that doesn't match any of the ones listed
    # in https://spdx.org/licenses/, but similar to Creative Commons?
    license("https://github.com/MCSclimate/MCT/blob/master/LICENSE")

    version("2.11.0", sha256="1b2a30bcba0081226ff1f1f5152e82afa3a2bb911215883965e669f776dcb365")
    version("2.10.0", sha256="42f32e3ab8bba31d16a1c6c9533f717a9d950e42c9b03b864b3436335d4e1b71")

    depends_on("mpi")
