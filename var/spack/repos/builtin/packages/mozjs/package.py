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


class Mozjs(AutotoolsPackage):
    """SpiderMonkey is Mozilla's JavaScript engine written in C/C++.
    It is used in various Mozilla products, including Firefox, and is
    available under the MPL2."""

    homepage = "https://developer.mozilla.org/en-US/docs/Mozilla/Projects/SpiderMonkey"

    version('24.2.0', '5db79c10e049a2dc117a6e6a3bc78a8e',
            url="http://ftp.mozilla.org/pub/js/mozjs-24.2.0.tar.bz2")
    version('17.0.0', '20b6f8f1140ef6e47daa3b16965c9202',
            url="http://ftp.mozilla.org/pub/js/mozjs17.0.0.tar.gz")
    version('1.8.5',  'a4574365938222adca0a6bd33329cb32',
            url="http://ftp.mozilla.org/pub/js/js185-1.0.0.tar.gz")

    depends_on('perl@5.6:', type='build')
    depends_on('pkgconfig', type='build')
    depends_on('python@2.7.3:2.8', type='build')
    depends_on('nspr', when='@:27')
    depends_on('libffi@3.0.9:')
    depends_on('readline')
    depends_on('zlib@1.2.3')

    configure_directory = 'js/src'
    build_directory = 'js/src/spack-build'

    patch('perl-bug.patch')

    def configure_args(self):
        spec = self.spec
        return [
            '--enable-readline',    # enables readline support in JS shell
            '--enable-threadsafe',  # enables support for multiple threads
            '--enable-system-ffi',
            '--with-system-zlib={0}'.format(spec['zlib'].prefix),
            '--with-system-nspr',
            '--with-nspr-prefix={0}'.format(spec['nspr'].prefix),
        ]
