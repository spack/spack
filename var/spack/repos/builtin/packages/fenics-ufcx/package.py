# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class FenicsUfcx(CMakePackage):
    """FFCx provides the ufcx.h interface header for finite element kernels,
    used by DOLFINx. ufcx.h can be installed from the FFCx repo without
    making it dependent on Python.
    """

    homepage = "https://github.com/FEniCS/ffcx"
    git = "https://github.com/FEniCS/ffcx.git"
    url = "https://github.com/FEniCS/ffcx/archive/v0.4.2.tar.gz"
    maintainers = ["ma595"]

    version("main", branch="main")
    version("0.5.0", sha256="3413409e5885e41e220f99e0f95cc817e94c4931143d1f700c6e0c5e1bfad1f6")
    version("0.4.2", sha256="3be6eef064d6ef907245db5b6cc15d4e603762e68b76e53e099935ca91ef1ee4")

    root_cmakelists_dir = "cmake"
