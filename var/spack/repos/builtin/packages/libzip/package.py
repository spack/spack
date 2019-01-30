# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Libzip(AutotoolsPackage):
    """libzip is a C library for reading, creating,
    and modifying zip archives."""

    homepage = "https://nih.at/libzip/index.html"
    url      = "https://nih.at/libzip/libzip-1.2.0.tar.gz"

    version('1.2.0', '5c3372ab3a7897295bfefb27f745cf69')
