# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Dnstracer(AutotoolsPackage):
    """Dnstracer determines where a given Domain Name Server gets
    its information from, and follows the chain of DNS servers back to
    the servers which know the data."""

    homepage = "https://github.com/Orc/dnstracer"
    git      = "https://github.com/Orc/dnstracer.git"

    version('master', branch='master')

    depends_on('autoconf', type='build')
    depends_on('automake', type='build')
    depends_on('libtool',  type='build')
    depends_on('m4',       type='build')

    phases = ['configure', 'build', 'install']
    def configure(self, spec, prefix):
        configure = Executable('./configure.sh')
        configure('--prefix={0}'.format(prefix))
