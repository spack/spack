##############################################################################
# Copyright (c) 2013-2018, Lawrence Livermore National Security, LLC.
# Produced at the Lawrence Livermore National Laboratory.
#
# This file is part of Spack.
# Created by Todd Gamblin, tgamblin@llnl.gov, All rights reserved.
# LLNL-CODE-647188
#
# For details, see https://github.com/spack/spack
# Please also see the NOTICE and LICENSE files for our notice and the LGPL.
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License (as
# published by the Free Software Foundation) version 2.1, February 1999.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the IMPLIED WARRANTY OF
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the terms and
# conditions of the GNU Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public
# License along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA 02111-1307 USA
##############################################################################

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
