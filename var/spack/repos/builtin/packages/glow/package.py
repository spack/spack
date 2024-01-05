# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Glow(Package):
    """
    Glow is a terminal based markdown reader designed
    from the ground up to bring out the beauty—and power—of the CLI.
    Use it to discover markdown files,
    read documentation directly on the command line and stash markdown files
    to your own private collection, so you can read them anywhere.
    Glow will find local markdown files in subdirectories or a local Git repository.
    """

    homepage = "https://github.com/charmbracelet/glow"
    url = "https://github.com/charmbracelet/glow/releases/download/v1.5.1/glow_Linux_x86_64.tar.gz"

    license("MIT")

    version("1.5.1", sha256="d224be006fc4ee361c1d1a85dbd46c269372b76c5413e2a9bfd0f7fe52c66f78")

    def install(self, spec, prefix):
        mkdirp(prefix.bin)
        install("glow", prefix.bin)
        mkdirp(prefix.completions)
        install_tree(".", prefix.completions)
