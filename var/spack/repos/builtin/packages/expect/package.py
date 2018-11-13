# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *
import glob
import os


class Expect(AutotoolsPackage):
    """Expect is a tool for automating interactive applications such as
    telnet, ftp, passwd, fsck, rlogin, tip, etc."""

    homepage = "http://expect.sourceforge.net/"
    url      = "https://sourceforge.net/projects/expect/files/Expect/5.45/expect5.45.tar.gz/download"

    version('5.45', '44e1a4f4c877e9ddc5a542dfa7ecc92b')

    depends_on('tcl')

    depends_on('automake', type='build')
    depends_on('autoconf', type='build')
    depends_on('libtool',  type='build')
    depends_on('m4',       type='build')

    force_autoreconf = True

    patch('expect_detect_tcl_private_header_os_x_mountain_lion.patch', when='@5.45')

    def configure_args(self):
        spec = self.spec

        args = [
            # Without this, expect binary and library are not installed
            '--exec-prefix={0}'.format(self.prefix),
            '--enable-threads',
            '--enable-shared',
            '--enable-64bit',
            '--with-tcl={0}'.format(spec['tcl'].prefix.lib),
            '--with-tclinclude={0}'.format(spec['tcl'].prefix.include),
        ]

        return args

    @run_after('install')
    def symlink_library(self):
        """Expect installs libraries into:

        lib/expect5.45/libexpect5.45.so

        Create a symlink so that the library can be found in lib."""

        target = join_path(self.prefix.lib, 'expect*', 'libexpect*')
        target = glob.glob(target)[0]

        link_name = os.path.basename(target)
        link_name = join_path(self.prefix.lib, link_name)

        symlink(target, link_name)
