# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Ed(AutotoolsPackage):
    """GNU ed is a line-oriented text editor. It is used to create,
       display, modify and otherwise manipulate text files, both
       interactively and via shell scripts."""

    homepage = "https://www.gnu.org/software/ed"
    url      = "https://ftpmirror.gnu.org/ed/ed-1.4.tar.gz"

    version('1.4', 'da0ddc0e0b0bec2da4b13b0d0d1bce2b')

    parallel = False
