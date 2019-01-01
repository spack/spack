# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Unibilium(Package):
    """A terminfo parsing library"""
    homepage = "https://github.com/mauke/unibilium"
    url      = "https://github.com/mauke/unibilium/archive/v1.2.0.tar.gz"

    version('1.2.0', '9b1c97839a880a373da6c097443b43c4')

    depends_on('libtool', type='build')

    def install(self, spec, prefix):
        make("PREFIX=" + prefix)
        make("install", "PREFIX=" + prefix)
