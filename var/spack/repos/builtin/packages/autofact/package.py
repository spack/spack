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


class Autofact(Package):
    """An Automatic Functional Annotation and Classification Tool"""

    homepage = "http://megasun.bch.umontreal.ca/Software/AutoFACT.htm"
    url      = "http://megasun.bch.umontreal.ca/Software/AutoFACT_v3_4.tar"

    version('3_4', sha256='1465d263b19adb42f01f6e636ac40ef1c2e3dbd63461f977b89da9493fe9c6f4')

    depends_on('perl', type='run')
    depends_on('perl-bio-perl', type='run')
    depends_on('perl-io-string', type='run')
    depends_on('perl-lwp', type='run')
    depends_on('blast-plus', type='run')

    def patch(self):
        with working_dir('scripts'):
            files = glob.iglob("*.pl")
            for file in files:
                change = FileFilter(file)
                change.filter('usr/bin/perl', 'usr/bin/env perl')

    def install(self, spec, prefix):
        install_tree(self.stage.source_path, prefix)

    def setup_environment(self, spack_env, run_env):
        run_env.prepend_path('PATH', self.prefix.scripts)
        run_env.set('PATH2AUTOFACT', self.prefix)
