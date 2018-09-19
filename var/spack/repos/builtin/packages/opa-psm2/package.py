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


class OpaPsm2(MakefilePackage):
    """ Intel Omni-Path Performance Scaled Messaging 2 (PSM2) library"""

    homepage = "http://github.com/01org/opa-psm2"
    url      = "https://github.com/01org/opa-psm2/archive/PSM2_10.3-8.tar.gz"

    version('10.3-37',  '9bfca04f29b937b3856f893e1f8b1b60')
    version('10.3-17',  'e7263eb449939cb87612e2c7623ca21c')
    version('10.3-10',  '59d36b49eb126f980f3272a9d66a8e98')
    version('10.3-8',   '07bc5cb2a6bf1189a29cbea836843db2')
    version('10.2-260', '71df31b5776be64ff243417ac88eec66')
    version('10.2-235', '23539f725a597bf2d35aac47a793a37b')
    version('10.2-175', 'c542b8641ad573f08f61d0a6a70f4013')

    depends_on('numactl')

    def setup_environment(self, spack_env, run_env):
        spack_env.set('DESTDIR', self.prefix)
        run_env.prepend_path('CPATH',
                             join_path(self.prefix, 'usr', 'include'))
        run_env.prepend_path('LIBRARY_PATH',
                             join_path(self.prefix, 'usr', 'lib64'))
        run_env.prepend_path('LD_LIBRARY_PATH',
                             join_path(self.prefix, 'usr', 'lib64'))

    def install(self, spec, prefix):
        make('--environment-overrides', 'install')
