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
import glob
import os
import sys


class Alglib(MakefilePackage):
    """ALGLIB is a cross-platform numerical analysis and data processing
    library."""

    homepage = "http://www.alglib.net"
    url      = "http://www.alglib.net/translator/re/alglib-3.11.0.cpp.gpl.tgz"

    version('3.11.0', 'f87bb05349924d486e8809590dee9f80')

    def url_for_version(self, version):
        return 'http://www.alglib.net/translator/re/alglib-{0}.cpp.gpl.tgz'.format(version.dotted)

    build_directory = 'src'

    def edit(self, spec, prefix):
        # this package has no build system!
        make_file_src = join_path(os.path.dirname(self.module.__file__),
                                  'Makefile')
        make_file = join_path(self.stage.source_path, 'src', 'Makefile')
        copy(make_file_src, make_file)
        filter_file(r'so', dso_suffix, make_file)

    def install(self, spec, prefix):
        name = 'libalglib.{0}'.format(dso_suffix)
        with working_dir('src'):
            mkdirp(prefix.lib)
            install(name, prefix.lib)
            mkdirp(prefix.include)
            headers = glob.glob('*.h')
            for h in headers:
                install(h, prefix.include)

    @run_after('install')
    def fix_darwin_install(self):
        # The shared libraries are not installed correctly on Darwin:
        if sys.platform == 'darwin':
            fix_darwin_install_name(self.spec.prefix.lib)
