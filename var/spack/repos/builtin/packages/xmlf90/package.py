# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack import *


class Xmlf90(AutotoolsPackage):
    """xmlf90 is a suite of libraries to handle XML in Fortran."""

    homepage = "https://launchpad.net/xmlf90"
    url      = "https://launchpad.net/xmlf90/trunk/1.5/+download/xmlf90-1.5.2.tgz"

    version('1.5.2', '324fdcba7dafce83db26e72aab9f6656')

    depends_on('autoconf@2.69:', type='build')
    depends_on('automake@1.14:', type='build')
    depends_on('libtool@2.4.2:', type='build')
    depends_on('m4',             type='build')

    def autoreconf(self, spec, prefix):
        sh = which('sh')
        sh('autogen.sh')

    def configure_args(self):
        if self.spec.satisfies('%gcc'):
            return ['FCFLAGS=-ffree-line-length-none']
        return []

    @run_after('install')
    def fix_mk(self):
        install(join_path(self.prefix, 'share', 'org.siesta-project',
                          'xmlf90.mk'), prefix)
