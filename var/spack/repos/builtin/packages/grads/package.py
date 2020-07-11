# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
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
#     spack install grads
#
# You can edit this file again by typing:
#
#     spack edit grads
#
# See the Spack documentation for more information on packaging.
# ----------------------------------------------------------------------------

from spack import *


class Grads(AutotoolsPackage):
    """FIXME: Put a proper description of your package here."""

    # FIXME: Add a proper url for your package's homepage here.
    homepage = "https://www.example.com"
    url      = "ftp://cola.gmu.edu/grads/2.2/grads-2.2.1-src.tar.gz"

    # FIXME: Add a list of GitHub accounts to
    # notify when the package is updated.
    # maintainers = ['github_user1', 'github_user2']

    version('2.2.1', sha256='695e2066d7d131720d598bac0beb61ac3ae5578240a5437401dc0ffbbe516206')

    depends_on('libgd')
    depends_on('libxmu')
    depends_on('cairo +X +pdf +fc +ft')
    depends_on('pkgconfig')
    depends_on('readline')

    def setup_environment(self, spack_env, run_env):
        spack_env.set('SUPPLIBS', '/')
        run_env.set('GADDIR', join_path(self.prefix, 'data'))
    
    @run_after('install')
    def copy_data(self):
        with working_dir(self.build_directory):
            install_tree('data', join_path(self.prefix, 'data'))
        with working_dir(self.package_dir):
            copy('udpt', join_path(self.prefix, 'data'))
            filter_file(r'({lib})', join_path(self.prefix, 'lib'), join_path(self.prefix, 'data/udpt'))

    """
    def configure_args(self):
        args = []
        args.append('--exec-prefix={0}'.format(self.prefix))
        args.append('--enable-dyn-supplibs=yes')
        args.append('--with-gnu-ld')
        args.append('--with-sysroot=/')
        return args
    """
