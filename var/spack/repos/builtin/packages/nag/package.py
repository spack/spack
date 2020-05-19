# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *
import os


class Nag(Package):
    """The NAG Fortran Compiler."""
    homepage = "http://www.nag.com/nagware/np.asp"
    maintainers = ['ThemosTsikas']

    version('7.0', sha256='bd53c988efe4bfd476a5f556ebd2b8924dc2a039f485e8e017581bca4e12ba01')
    version('6.2', sha256='9b60f6ffa4f4be631079676963e74eea25e8824512e5c864eb06758b2a3cdd2d')
    version('6.1', sha256='32580e0004e6798abf1fa52f0070281b28abeb0da2387530a4cc41218e813c7c')

    # Licensing
    license_required = True
    license_comment = '!'
    license_files = ['lib/nag.key']
    license_vars = ['NAG_KUSARI_FILE']
    license_url = 'http://www.nag.com/doc/inun/np61/lin-mac/klicence.txt'

    def url_for_version(self, version):
        # TODO: url and checksum are architecture dependent
        # TODO: We currently only support x86_64
        url = 'https://www.nag.com/downloads/impl/npl6a{0}na_amd64.tgz'
        return url.format(version.joined)

    def install(self, spec, prefix):
        # Set installation directories
        os.environ['INSTALL_TO_BINDIR'] = prefix.bin
        os.environ['INSTALL_TO_LIBDIR'] = prefix.lib
        os.environ['INSTALL_TO_MANDIR'] = prefix + '/share/man/man'

        # Run install script
        os.system('./INSTALLU.sh')

    def setup_run_environment(self, env):
        env.set('F77', self.prefix.bin.nagfor)
        env.set('FC',  self.prefix.bin.nagfor)
