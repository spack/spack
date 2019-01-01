# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *
import os


class Nag(Package):
    """The NAG Fortran Compiler."""
    homepage = "http://www.nag.com/nagware/np.asp"

    version('6.2', '8b119cc3296969bbd68b781f625de272')
    version('6.1', '9b3cc0f8703c79f6231ae12359535119')
    version('6.0', '3fa1e7f7b51ef8a23e6c687cdcad9f96')

    # Licensing
    license_required = True
    license_comment = '!'
    license_files = ['lib/nag.key']
    license_vars = ['NAG_KUSARI_FILE']
    license_url = 'http://www.nag.com/doc/inun/np61/lin-mac/klicence.txt'

    def url_for_version(self, version):
        # TODO: url and checksum are architecture dependent
        # TODO: We currently only support x86_64
        url = 'http://www.nag.com/downloads/impl/npl6a{0}na_amd64.tgz'
        return url.format(version.joined)

    def install(self, spec, prefix):
        # Set installation directories
        os.environ['INSTALL_TO_BINDIR'] = prefix.bin
        os.environ['INSTALL_TO_LIBDIR'] = prefix.lib
        os.environ['INSTALL_TO_MANDIR'] = prefix + '/share/man/man'

        # Run install script
        os.system('./INSTALLU.sh')

    def setup_environment(self, spack_env, run_env):
        run_env.set('F77', join_path(self.prefix.bin, 'nagfor'))
        run_env.set('FC',  join_path(self.prefix.bin, 'nagfor'))
