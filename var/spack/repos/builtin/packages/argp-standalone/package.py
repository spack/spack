# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack import *


class ArgpStandalone(AutotoolsPackage):
    """Standalone version of the argp interface from glibc for parsing
       unix-style arguments. """

    homepage = "https://www.lysator.liu.se/~nisse/misc"
    url      = "https://www.lysator.liu.se/~nisse/misc/argp-standalone-1.3.tar.gz"

    version('1.3', '720704bac078d067111b32444e24ba69')

    # Homebrew (https://github.com/Homebrew/homebrew-core) patches
    # argp-standalone to work on Darwin; the patchfile below was taken
    # from
    # https://raw.githubusercontent.com/Homebrew/formula-patches/b5f0ad3/argp-standalone/patch-argp-fmtstream.h
    patch('argp-fmtstream.h.patch', 0, 'platform=darwin', '.')

    def install(self, spec, prefix):
        make('install')
        make('check')
        mkdirp(self.spec.prefix.lib)
        install('libargp.a', join_path(self.spec.prefix.lib, 'libargp.a'))
        mkdirp(self.spec.prefix.include)
        install('argp.h', join_path(self.spec.prefix.include, 'argp.h'))
