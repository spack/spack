# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class JsonCwx(AutotoolsPackage):
    """JSON-C with Extensions"""

    homepage = "https://github.com/LLNL/json-cwx"
    url      = "https://github.com/LLNL/json-cwx/archive/0.12.tar.gz"

    version('0.12', '8ba44ef7f463f004b4b14c6d8d85a2b70db977a4')

    depends_on('autoconf', type='build')
    depends_on('automake', type='build')
    depends_on('libtool',  type='build')
    depends_on('m4',       type='build')

    parallel = False

    configure_directory = 'json-cwx'

    def autoreconf(self, spec, prefix):
        with working_dir('json-cwx'):
            autogen = Executable("./autogen.sh")
            autogen()
