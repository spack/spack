# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class AlsaLib(AutotoolsPackage):
    """The Advanced Linux Sound Architecture (ALSA) provides audio and MIDI
    functionality to the Linux operating system. alsa-lib contains the user
    space library that developers compile ALSA applications against."""

    homepage = "https://www.alsa-project.org"
    url      = "ftp://ftp.alsa-project.org/pub/lib/alsa-lib-1.1.4.1.tar.bz2"

    version('1.1.4.1', '29fa3e69122d3cf3e8f0e01a0cb1d183')
