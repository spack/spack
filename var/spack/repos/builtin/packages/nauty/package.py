##############################################################################
# Copyright (c) 2013-2017, Lawrence Livermore National Security, LLC.
# Produced at the Lawrence Livermore National Laboratory.
#
# This file is part of Spack.
# Created by Todd Gamblin, tgamblin@llnl.gov, All rights reserved.
# LLNL-CODE-647188
#
# For details, see https://github.com/llnl/spack
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

import os
from spack import *


class Nauty(AutotoolsPackage):
    """nauty and Traces are programs for computing automorphism groups of
    graphsq and digraphs"""
    homepage = "http://pallini.di.uniroma1.it/index.html"
    url      = "http://pallini.di.uniroma1.it/nauty26r7.tar.gz"

    version('2.6r7', 'b2b18e03ea7698db3fbe06c5d76ad8fe')

    # Debian/ Fedora patches for @2.6r7:
    urls_for_patches = {
        '@2.6r7': [
            # Debian patch to fix the gt_numorbits declaration
            ('https://src.fedoraproject.org/rpms/nauty/raw/0f07d01caf84e9d30cb06b11af4860dd3837636a/f/nauty-fix-gt_numorbits.patch', 'a6e1ef4897aabd67c104fd1d78bcc334'),  # noqa: E50
            # Debian patch to add explicit extern declarations where needed
            ('https://src.fedoraproject.org/rpms/nauty/raw/0f07d01caf84e9d30cb06b11af4860dd3837636a/f/nauty-fix-include-extern.patch', '741034dec2d2f8b418b6e186aa3eb50f'),  # noqa: E50
            # Debian patch to use zlib instead of invoking zcat through a pipe
            ('https://src.fedoraproject.org/rpms/nauty/raw/0f07d01caf84e9d30cb06b11af4860dd3837636a/f/nauty-zlib-blisstog.patch', '667e1ce341f2506482ad30afd04f17e3'),  # noqa: E50
            # Debian patch to improve usage and help information
            ('https://src.fedoraproject.org/rpms/nauty/raw/0f07d01caf84e9d30cb06b11af4860dd3837636a/f/nauty-help2man.patch', '4202e6d83362daa2c4c4ab0788e11ac5'),  # noqa: E50
            # Debian patch to add libtool support for building a shared library
            ('https://src.fedoraproject.org/rpms/nauty/raw/0f07d01caf84e9d30cb06b11af4860dd3837636a/f/nauty-autotoolization.patch', 'ea75f19c8a980c4d6d4e07223785c751'),  # noqa: E50
            # Debian patch to canonicalize header file usage
            ('https://src.fedoraproject.org/rpms/nauty/raw/0f07d01caf84e9d30cb06b11af4860dd3837636a/f/nauty-includes.patch', 'c6ce4209d1381fb5489ed552ef35d7dc'),  # noqa: E50
            # Debian patch to prefix "nauty-" to the names of the generic tools
            ('https://src.fedoraproject.org/rpms/nauty/raw/0f07d01caf84e9d30cb06b11af4860dd3837636a/f/nauty-tool-prefix.patch', 'e89d87b4450adc5d0009ce11438dc975'),  # noqa: E50
            # Fedora patch to detect availability of the popcnt
            # instruction at runtime
            ('https://src.fedoraproject.org/rpms/nauty/raw/0f07d01caf84e9d30cb06b11af4860dd3837636a/f/nauty-popcnt.patch', '8a32d31a7150c8f5f21ccb1f6dc857b1')  # noqa: E50
        ]
    }
    # Iterate over patches
    for condition, urls in urls_for_patches.items():
        for url, md5 in urls:
            patch(url, when=condition, level=1, md5=md5)

    depends_on('m4',  type='build', when='@2.6r7')
    depends_on('autoconf',  type='build', when='@2.6r7')
    depends_on('automake',  type='build', when='@2.6r7')
    depends_on('libtool',  type='build', when='@2.6r7')
    depends_on('pkg-config',  type='build')
    depends_on('zlib')

    @property
    def force_autoreconf(self):
        return self.spec.satisfies('@2.6r7')

    def url_for_version(self, version):
        url = "http://pallini.di.uniroma1.it/nauty{0}.tar.gz"
        return url.format(version.joined)

    def patch(self):
        os.remove('makefile')
        ver = str(self.version.dotted).replace('r', '.')
        if self.spec.satisfies('@2.6r7'):
            filter_file('@INJECTVER@', ver, "configure.ac")
