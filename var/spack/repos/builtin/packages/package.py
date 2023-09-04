# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class TimeWarrior(CMakePackage):
    """Free and Open Source Software that tracks time from the command line."""

    homepage = "https://timewarrior.net/"
    url = "https://github.com/GothenburgBitFactory/timewarrior/releases/download/v1.5.0/timew-1.5.0.tar.gz"

    version("1.5.0", sha256="51e7c2c772837bbd6d56da8d16506c4b6de8644166e0b5234ad36ae6a70dd4f6")

    depends_on("cmake@2.8:", type="build")
    depends_on("uuid")

    conflicts("%gcc@:4.7")
