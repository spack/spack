# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class AmdAocl(BundlePackage):
    """AMD Optimizing CPU Libraries (AOCL) - AOCL is a set of numerical
    libraries tuned specifically for AMD EPYC processor family. They have a
    simple interface to take advantage of the latest hardware innovations.
    The tuned implementations of industry standard  math libraries enable
    fast development of scientific and high performance computing projects

    LICENSING INFORMATION: By downloading, installing and using this software,
    you agree to the terms and conditions of the AMD AOCL license agreement.
    You may obtain a copy of this license agreement from
    https://www.amd.com/en/developer/aocl/aocl-eula.html
    https://www.amd.com/en/developer/aocl/aocl-4-0-eula.html
    """

    homepage = "https://developer.amd.com/amd-aocl/"

    maintainers("amd-toolchain-support")

    version("4.0")
    version("3.2")
    version("3.1")
    version("3.0")
    version("2.2")

    variant("openmp", default=False, description="Enable OpenMP support.")

    for vers in ["2.2", "3.0", "3.1", "3.2", "4.0"]:
        depends_on("amdblis@{0} threads=openmp".format(vers), when="@{0} +openmp".format(vers))
        depends_on("amdblis@{0} threads=none".format(vers), when="@{0} ~openmp".format(vers))
        depends_on("amdfftw@{0} +openmp".format(vers), when="@{0} +openmp".format(vers))
        depends_on("amdfftw@{0} ~openmp".format(vers), when="@{0} ~openmp".format(vers))
        depends_on("amdlibflame@{0}".format(vers), when="@{0}".format(vers))
        depends_on("amdlibm@{0}".format(vers), when="@{0}".format(vers))
        depends_on(
            "amdscalapack@{0} ^amdblis@{0} threads=none".format(vers),
            when="@{0} ~openmp".format(vers),
        )
        depends_on(
            "amdscalapack@{0} ^amdblis@{0} threads=openmp".format(vers),
            when="@{0} +openmp".format(vers),
        )
        depends_on("aocl-sparse@{0}".format(vers), when="@{0}".format(vers))
