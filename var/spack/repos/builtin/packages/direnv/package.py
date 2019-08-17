# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Direnv(Package):
    """direnv is an environment switcher for the shell."""

    homepage = "https://direnv.net/"
    url      = "https://github.com/direnv/direnv/archive/v2.11.3.tar.gz"

    version('2.11.3', '5b9728e2dabed232b4932849647fd6e5')

    depends_on('go', type='build')

    def install(self, spec, prefix):
        make('install', "DESTDIR=%s" % prefix)
