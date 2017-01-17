##############################################################################
# Copyright (c) 2013-2016, Lawrence Livermore National Security, LLC.
# Produced at the Lawrence Livermore National Laboratory.
#
# This file is part of Spack.
# Created by Todd Gamblin, tgamblin@llnl.gov, All rights reserved.
# LLNL-CODE-647188
#
# For details, see https://github.com/llnl/spack
# Please also see the LICENSE file for our notice and the LGPL.
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
import llnl.util.tty as tty
import os


class Mercurial(Package):
    """Mercurial is a free, distributed source control management tool."""

    homepage = "https://www.mercurial-scm.org"
    url      = "https://www.mercurial-scm.org/release/mercurial-3.9.tar.gz"

    version('3.9.1', '3759dd10edb8c1a6dfb8ff0ce82658ce')
    version('3.9',   'e2b355da744e94747daae3a5339d28a0')
    version('3.8.4', 'cec2c3db688cb87142809089c6ae13e9')
    version('3.8.3', '97aced7018614eeccc9621a3dea35fda')
    version('3.8.2', 'c38daa0cbe264fc621dc3bb05933b0b3')
    version('3.8.1', '172a8c588adca12308c2aca16608d7f4')

    extends('python')
    depends_on('python@2.6:2.8')
    depends_on('py-docutils', type='build')

    def install(self, spec, prefix):
        make('install', 'PREFIX={0}'.format(prefix))

        # Configuration of HTTPS certificate authorities
        # https://www.mercurial-scm.org/wiki/CACertificates
        hgrc_filename = join_path(prefix.etc, 'mercurial', 'hgrc')
        mkdirp(os.path.dirname(hgrc_filename))

        with open(hgrc_filename, 'w') as hgrc:
            if os.path.exists('/etc/ssl/certs/ca-certificates.crt'):
                # Debian/Ubuntu/Gentoo/Arch Linux
                hgrc.write('[web]\ncacerts = /etc/ssl/certs/ca-certificates.crt')  # noqa
            elif os.path.exists('/etc/pki/tls/certs/ca-bundle.crt'):
                # Fedora/RHEL/CentOS
                hgrc.write('[web]\ncacerts = /etc/pki/tls/certs/ca-bundle.crt')
            elif os.path.exists('/etc/ssl/ca-bundle.pem'):
                # openSUSE/SLE
                hgrc.write('[web]\ncacerts = /etc/ssl/ca-bundle.pem')
            else:
                tty.warn('CA certificate not found. You may not be able to '
                         'connect to an HTTPS server. If your CA certificate '
                         'is in a non-standard location, you should add it to '
                         '{0}'.format(hgrc_filename))
