# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Fish(CMakePackage):
    """fish is a smart and user-friendly command line shell for OS X, Linux, and
    the rest of the family.
    """

    homepage = "https://fishshell.com/"
    url      = "https://github.com/fish-shell/fish-shell/releases/download/2.7.1/fish-2.7.1.tar.gz"
    list_url = "https://fishshell.com/"

    depends_on('ncurses')

    version('3.1.0', sha256='e5db1e6839685c56f172e1000c138e290add4aa521f187df4cd79d4eab294368')
    version('3.0.0', sha256='ea9dd3614bb0346829ce7319437c6a93e3e1dfde3b7f6a469b543b0d2c68f2cf')
