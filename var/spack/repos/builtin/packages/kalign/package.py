# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class Kalign(AutotoolsPackage):
    """A fast multiple sequence alignment program for biological sequences."""

    homepage = "https://github.com/TimoLassmann/kalign"
    url = "https://github.com/TimoLassmann/kalign/archive/refs/tags/v3.3.1.tar.gz"

    version("3.3.1", sha256="7f10acf9a3fa15deabbc0304e7c14efa25cea39108318c9f02b47257de2d7390")

    depends_on("autoconf", type="build")
    depends_on("automake", type="build")
    depends_on("libtool", type="build")
