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
    maintainers = ["ma595", "jhale"]

    version("main", branch="main")
    version("0.5.0.post0", sha256="039908c9998b51ba53e5deb3a97016062c262f0a4285218644304f7d3cd35882")
    version("0.4.2", sha256="3be6eef064d6ef907245db5b6cc15d4e603762e68b76e53e099935ca91ef1ee4")

    depends_on("cmake@3.19:", type="build")

    root_cmakelists_dir = "cmake"
