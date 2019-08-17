# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class GnuProlog(Package):
    """A free Prolog compiler with constraint solving over finite domains."""
    homepage = "http://www.gprolog.org/"
    url      = "http://www.gprolog.org/gprolog-1.4.4.tar.gz"

    version('1.4.4', '37009da471e5217ff637ad1c516448c8')

    parallel = False

    def install(self, spec, prefix):
        with working_dir('src'):
            configure('--with-install-dir=%s' % prefix,
                      '--without-links-dir')
            make()
            make('install')
