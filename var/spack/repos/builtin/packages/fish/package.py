# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Fish(AutotoolsPackage):
    """fish is a smart and user-friendly command line shell for OS X, Linux, and
    the rest of the family.
    """

    homepage = "https://fishshell.com/"
    url      = "https://github.com/fish-shell/fish-shell/releases/download/2.7.1/fish-2.7.1.tar.gz"
    list_url = "https://fishshell.com/"

    depends_on('ncurses')

    version('3.0.0', sha256='ea9dd3614bb0346829ce7319437c6a93e3e1dfde3b7f6a469b543b0d2c68f2cf')
    version('2.7.1', sha256='e42bb19c7586356905a58578190be792df960fa81de35effb1ca5a5a981f0c5a')
    version('2.7.0', sha256='3a76b7cae92f9f88863c35c832d2427fb66082f98e92a02203dc900b8fa87bcb')
    version('2.2.0', sha256='a76339fd14ce2ec229283c53e805faac48c3e99d9e3ede9d82c0554acfc7b77a')
