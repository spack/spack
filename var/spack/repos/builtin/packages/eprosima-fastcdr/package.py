# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class EprosimaFastcdr(CMakePackage):
    """eProsima Fast CDR is a C++ library that provides two serialization mechanisms.
    One is the standard CDR serialization mechanism, while the other is a
    faster implementation that modifies the standard."""

    homepage = "https://www.eprosima.com/"
    url = "https://github.com/eProsima/Fast-CDR/archive/v1.0.27.tar.gz"

    license("Apache-2.0")

    version("1.0.27", sha256="a9bc8fd31a2c2b95e6d2fb46e6ce1ad733e86dc4442f733479e33ed9cdc54bf6")
