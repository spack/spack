# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class Kalign(AutotoolsPackage, CMakePackage):
    """A fast multiple sequence alignment program for biological sequences."""

    homepage = "https://github.com/TimoLassmann/kalign"
    url = "https://github.com/TimoLassmann/kalign/archive/refs/tags/v3.3.1.tar.gz"

    version("3.3.5", sha256="75f3a127d2a9eef1eafd931fb0785736eb3f82826be506e7edd00daf1ba26212")
    version("3.3.2", sha256="c0b357feda32e16041cf286a4e67626a52bbf78c39e2237b485d54fb38ef319a")
    version("3.3.1", sha256="7f10acf9a3fa15deabbc0304e7c14efa25cea39108318c9f02b47257de2d7390")

    build_system(
        conditional("cmake", when="@3.3.4:"),
        conditional("autotools", when="@:3.3.2"),
        default="cmake",
    )

    depends_on("autoconf", type="build", when="@:3.3.2")
    depends_on("automake", type="build", when="@:3.3.2")
    depends_on("libtool", type="build", when="@:3.3.2")
