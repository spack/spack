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
from llnl.util import tty


class Mercurial(PythonPackage):
    """Mercurial is a free, distributed source control management tool."""

    homepage = "https://www.mercurial-scm.org"
    url      = "https://www.mercurial-scm.org/release/mercurial-4.1.2.tar.gz"

    import_modules = [
        'hgext', 'hgext3rd', 'mercurial', 'hgext.convert', 'hgext.fsmonitor',
        'hgext.highlight', 'hgext.largefiles', 'hgext.zeroconf',
        'hgext.fsmonitor.pywatchman', 'mercurial.hgweb',
        'mercurial.httpclient', 'mercurial.pure'
    ]

    version('4.4.1', '37974a416d1d9525e1375c92025b16d9')
    version('4.1.2', '934c99808bdc8385e074b902d59b0d93')
    version('3.9.1', '3759dd10edb8c1a6dfb8ff0ce82658ce')
    version('3.9',   'e2b355da744e94747daae3a5339d28a0')
    version('3.8.4', 'cec2c3db688cb87142809089c6ae13e9')
    version('3.8.3', '97aced7018614eeccc9621a3dea35fda')
    version('3.8.2', 'c38daa0cbe264fc621dc3bb05933b0b3')
    version('3.8.1', '172a8c588adca12308c2aca16608d7f4')

    depends_on('python@2.6:2.8', when='@:4.2.99')
    depends_on('python@2.7:2.8,3.5:3.5.999,3.6.2:', when='@4.3:')
    depends_on('py-docutils', type='build')
    depends_on('py-pygments', type=('build', 'run'))
    depends_on('py-certifi',  type=('build', 'run'))

    @run_after('install')
    def post_install(self):
        prefix = self.prefix

        # Install man pages
        mkdirp(prefix.man.man1)
        mkdirp(prefix.man.man5)
        mkdirp(prefix.man.man8)
        with working_dir('doc'):
            install('hg.1', prefix.man.man1)
            install('hgignore.5', prefix.man.man5)
            install('hgrc.5', prefix.man.man5)
            install('hg-ssh.8', prefix.man.man8)

        # Install completion scripts
        contrib = join_path(prefix, 'contrib')
        mkdir(contrib)
        with working_dir('contrib'):
            install('bash_completion', join_path(contrib, 'bash_completion'))
            install('zsh_completion',  join_path(contrib, 'zsh_completion'))

    @run_after('install')
    def configure_certificates(self):
        """Configuration of HTTPS certificate authorities
        https://www.mercurial-scm.org/wiki/CACertificates"""

        etc_dir = join_path(self.prefix.etc, 'mercurial')
        mkdirp(etc_dir)

        hgrc_filename = join_path(etc_dir, 'hgrc')

        # Use certifi to find the location of the CA certificate
        print_str = self.spec['python'].package.print_string('certifi.where()')
        certificate = python('-c', 'import certifi; ' + print_str)

        if not certificate:
            tty.warn('CA certificate not found. You may not be able to '
                     'connect to an HTTPS server. If your CA certificate '
                     'is in a non-standard location, you should add it to '
                     '{0}.'.format(hgrc_filename))

        # Write the global mercurial configuration file
        with open(hgrc_filename, 'w') as hgrc:
            hgrc.write('[web]\ncacerts = {0}'.format(certificate))

    @run_after('install')
    @on_package_attributes(run_tests=True)
    def check_install(self):
        """Sanity-check setup."""

        hg = Executable(join_path(self.prefix.bin, 'hg'))

        hg('debuginstall')
        hg('version')
