# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Codec2(CMakePackage):
    """Open source speech codec designed for communications quality speech
    between 450 and 3200 bit/s. The main application is low bandwidth
    HF/VHF digital radio."""

    homepage = "https://www.rowetel.com/?page_id=452"
    url = "https://github.com/drowe67/codec2/archive/v0.9.2.tar.gz"

    license("LGPL-2.1-or-later")

    version("1.1.0", sha256="d56ba661008a780b823d576a5a2742c94d0b0507574643a7d4f54c76134826a3")
    version("1.0.5", sha256="cd9a065dd1c3477f6172a0156294f767688847e4d170103d1f08b3a075f82826")
    version("0.9.2", sha256="19181a446f4df3e6d616b50cabdac4485abb9cd3242cf312a0785f892ed4c76c")
