# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

# ----------------------------------------------------------------------------
# If you submit this package back to Spack as a pull request,
# please first remove this boilerplate and all FIXME comments.
#
# This is a template package file for Spack.  We've put "FIXME"
# next to all the things you'll want to change. Once you've handled
# them, you can save this file and test your package like this:
#
#     spack install ntl
#
# You can edit this file again by typing:
#
#     spack edit ntl
#
# See the Spack documentation for more information on packaging.
# ----------------------------------------------------------------------------

from spack import *


class Ntl(Package):
    """
    NTL  -- a library for doing numbery theory --  version 11.5.1
    Release date: 2021.06.23

    Author: Victor Shoup (victor@shoup.net)

    NTL is open-source software distributed under the terms of the GNU Lesser
    General Public License (LGPL) version 2.1 or later.  See the file
    doc/copying.txt for complete details on the licensing of NTL.

    Documentation is available in the file doc/tour.html, which can be viewed
    with a web browser.

    For a detailed guide to installation, please see the appropriate
    documentation:
    * doc/tour-unix.html for unix systems
    * doc/tour-win.html for Windows systems

    The latest version of NTL is available at http://www.shoup.net.
    """

    homepage = "https://libntl.org"
    url      = "https://github.com/libntl/ntl/archive/refs/tags/v11.5.1.tar.gz"

    # notify when the package is updated.
    maintainers = ['wohlbier']

    version('11.5.1', sha256='ef578fa8b6c0c64edd1183c4c303b534468b58dd3eb8df8c9a5633f984888de5')
    version('11.5.0', sha256='9e1e6488b177c3e5d772fdd6279c890937a9d1c3b694a904ac1cfbe9cab836db')
    version('11.4.4', sha256='2ce7a10fadbed6c3859d72c859612a4ca0dbdf6a9db99db4261422b7f0804bfa')

    variant('shared', values=bool, default=False,
            description='Build shared library.')

    depends_on('gmp')

    phases = ['configure', 'build', 'install']

    def setup_environment(self, spack_env, run_env):
        spec = self.spec

    def configure_args(self):
        spec = self.spec
        prefix = self.prefix

        config_args = [
            'DEF_PREFIX={0}'.format(prefix),
            'GMP_PREFIX={0}'.format(spec['gmp'].prefix) # gmp dependency
        ]
        if '+shared' in spec:
            config_args.append('SHARED=on')

        return config_args

    def configure(self, spec, prefix):
        with working_dir('src'):
            configure = Executable('./configure')
            configure(*self.configure_args())

    def build(self, spec, prefix):
        with working_dir('src'):
            make()
            #make('check')

    def install(self, spec, prefix):
        with working_dir('src'):
            make('install')
