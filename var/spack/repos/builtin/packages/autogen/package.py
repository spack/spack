# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Autogen(AutotoolsPackage, GNUMirrorPackage):
    """AutoGen is a tool designed to simplify the creation and maintenance of
    programs that contain large amounts of repetitious text. It is especially
    valuable in programs that have several blocks of text that must be kept
    synchronized."""

    homepage = "https://www.gnu.org/software/autogen/index.html"
    gnu_mirror_path = "autogen/rel5.18.12/autogen-5.18.12.tar.gz"
    list_url = "https://ftp.gnu.org/gnu/autogen"
    list_depth = 1

    version('5.18.16', sha256='e23c5bbd0ac83079ae2ef6eb3fd1948fecce718ac853025607a3ab0395538406')
    version('5.18.14', sha256='93842ec26552b50e4f22d10bcc2b102e9fb9922ae68765801f1f043631b7db66')
    version('5.18.12', sha256='805c20182f3cb0ebf1571d3b01972851c56fb34348dfdc38799fd0ec3b2badbe')

    variant('xml', default=True, description='Enable XML support')

    depends_on('pkgconfig', type='build')

    depends_on('guile@1.8:2.0')
    depends_on('libxml2', when='+xml')

    def configure_args(self):
        spec = self.spec

        args = [
            # `make check` fails without this
            # Adding a gettext dependency does not help
            '--disable-nls',
        ]

        if '+xml' in spec:
            args.append('--with-libxml2={0}'.format(spec['libxml2'].prefix))
        else:
            args.append('--without-libxml2')

        return args
