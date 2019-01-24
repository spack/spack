# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

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
