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


class Intltool(AutotoolsPackage):
    """intltool is a set of tools to centralize translation of many different
    file formats using GNU gettext-compatible PO files."""

    homepage = 'https://freedesktop.org/wiki/Software/intltool/'
    url      = 'https://launchpad.net/intltool/trunk/0.51.0/+download/intltool-0.51.0.tar.gz'
    list_url = 'https://launchpad.net/intltool/+download'

    version('0.51.0', '12e517cac2b57a0121cda351570f1e63')

    # requires XML::Parser perl module
    depends_on('perl-xml-parser', type=('build', 'run'))
    depends_on('perl@5.8.1:',     type=('build', 'run'))

    # patch for "Unescaped left brace in regex is illegal here in regex"
    # warnings witn perl 5.22 and errors with perl 5.26 and newer
    patch('https://launchpadlibrarian.net/216052398/intltool-perl-5.22.patch',
          sha256='ca9d6562f29f06c64150f50369a24402b7aa01a3a0dc73dce55106f3224330a1',
          level=0)

    def check(self):
        # `make check` passes but causes `make install` to fail
        pass

    def _make_executable(self, name):
        return Executable(join_path(self.prefix.bin, name))

    def setup_dependent_package(self, module, dependent_spec):
        # intltool is very likely to be a build dependency,
        # so we add the tools it provides to the dependent module
        executables = [
            'intltool-extract',
            'intltoolize',
            'intltool-merge',
            'intltool-prepare',
            'intltool-update'
        ]

        for name in executables:
            setattr(module, name, self._make_executable(name))
