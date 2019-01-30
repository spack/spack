# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Libbsd(AutotoolsPackage):
    """This library provides useful functions commonly found on BSD
    systems, and lacking on others like GNU systems, thus making it easier
    to port projects with strong BSD origins, without needing to embed the
    same code over and over again on each project.
    """

    homepage = "https://libbsd.freedesktop.org/wiki/"
    url      = "https://libbsd.freedesktop.org/releases/libbsd-0.8.6.tar.xz"

    version('0.8.6', '4ab7bec639af17d0aacb50222b479110')

    patch('cdefs.h.patch', when='%gcc@:4')
