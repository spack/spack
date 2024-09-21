# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Bird(AutotoolsPackage):
    """The BIRD project aims to develop a dynamic IP routing daemon with
    full support of all modern routing protocols, easy to use
    configuration interface and powerful route filtering language,
    primarily targeted on (but not limited to) Linux and other UNIX-like
    systems and distributed under the GNU General Public License."""

    homepage = "https://bird.network.cz/"
    url = "https://gitlab.nic.cz/labs/bird/-/archive/v2.0.2/bird-v2.0.2.tar.gz"

    license("GPL-2.0-or-later", checked_by="wdconinc")

    version("2.15.1", sha256="5a4cf55c4767192aa57880ac5f6763e5b8c26f688ab5934df96e3615c4b0a1e1")
    version("2.0.2", sha256="e1e9ac92faf5893890c478386fdbd3c391ec2e9b911b1dfccec7b7fa825e9820")
    version("2.0.1", sha256="c222968bb017e6b77d14f4e778f437b84f4ccae686355a3ad8e88799285e7636")

    depends_on("c", type="build")
    depends_on("autoconf", type="build")
    depends_on("automake", type="build")
    depends_on("libtool", type="build")
    depends_on("m4", type="build")
    depends_on("flex", type="build")
    depends_on("bison", type="build")
    depends_on("ncurses")
    depends_on("readline")
