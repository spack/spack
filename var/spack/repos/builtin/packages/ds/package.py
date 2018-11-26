# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Ds(AutotoolsPackage):
    """SAOImage DS9 is an astronomical imaging and data visualization
       application."""

    homepage = "http://ds9.si.edu/"
    url      = "http://ds9.si.edu/download/source/ds9.8.0rc6.tar.gz"

    version('9.8.0rc6', sha256='9c926dbe5475529b4de456058605e61e523f442993a3aa188f5d3fbd59a9af7a')

    depends_on('autoconf', type='build')
    depends_on('automake', type='build')
    depends_on('m4', type='build')
    depends_on('libtool', type='build')

    depends_on('libx11', type=('build', 'link', 'run'))
    depends_on('libxml2', type=('build', 'link', 'run'))
    depends_on('libxslt', type=('build', 'link', 'run'))
    depends_on('openssl', type=('build', 'link', 'run'))
    depends_on('tcl', type=('build', 'link', 'run'))
    depends_on('tcl-tclxml', type=('build', 'link', 'run'))
    depends_on('tk', type=('build', 'link', 'run'))

    phases = ['configure', 'build', 'install']

    def patch(self):
        # the package provides it's own TCL utilities
        # compiling and manually setting paths for all of them is contrived
        # (most of the utilities are small and not included in spack)

        # inject libxml, libxslt prefixes into configure search paths
        filter_file('/usr/bin/xml2-config',
                    join_path(self.spec['libxml2'].prefix, 'bin/xml2-config'),
                    'tclxml/configure', string=True)

        filter_file('/usr/bin/xslt-config',
                    join_path(self.spec['libxslt'].prefix, 'bin/xslt-config'),
                    'tclxml/configure', string=True)

    def configure(self, spec, prefix):
        # no args needed, we can't pass any to the dependency configures anyway
        args = ['--prefix={0}'.format(prefix)]

        conf = Executable('unix/configure')
        conf(*args)

    def install(self, spec, prefix):
        # no install target provided in Makefile, install manually

        install_tree('bin', prefix.bin)
        install_tree('share', prefix.share)
        install_tree('lib', prefix.lib)
