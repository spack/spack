# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.pkgkit import *


class Xmlf90(AutotoolsPackage):
    """xmlf90 is a suite of libraries to handle XML in Fortran."""

    homepage = "https://launchpad.net/xmlf90"
    url      = "https://launchpad.net/xmlf90/trunk/1.5/+download/xmlf90-1.5.4.tar.gz"

    version('1.5.4', sha256='a0b1324ff224d5b5ad1127a6ad4f90979f6b127f1a517f98253eea377237bbe4')
    version('1.5.3', sha256='a5378a5d9df4b617f51382092999eb0f20fa1a90ab49afbccfd80aa51650d27c')
    version('1.5.2', sha256='666694db793828d1d1e9aea665f75c75ee21772693465a88b43e6370862abfa6')

    depends_on('autoconf@2.69:', type='build')
    depends_on('automake@1.14:', type='build')
    depends_on('libtool@2.4.2:', type='build')
    depends_on('m4',             type='build')

    def url_for_version(self, version):
        url = 'https://launchpad.net/xmlf90/trunk/{0}/+download/xmlf90-{1}.tar.gz'
        return url.format(version.up_to(2), version)

    @when('@1.5.2')
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
