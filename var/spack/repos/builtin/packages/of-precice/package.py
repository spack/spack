##############################################################################
# Copyright (c) 2018 Mark Olesen, OpenCFD Ltd.
#
# This file was authored by Mark Olesen <mark.olesen@esi-group.com>
# and is released as part of spack under the LGPL license.
# LLNL-CODE-647188
#
# For details, see https://github.com/spack/spack
# Please also see the NOTICE and LICENSE files for the LLNL notice and LGPL.
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
import os

import llnl.util.tty as tty

from spack import *
from spack.pkg.builtin.openfoam_com import add_extra_files


class OfPrecice(Package):
    """preCICE adapter for OpenFOAM"""

    homepage = 'https://www.precice.org'
    git      = 'https://github.com/precice/openfoam-adapter.git'

    # Currently develop only
    version('develop', branch='master')

    depends_on('openfoam+source')
    depends_on('precice')
    depends_on('yaml-cpp')

    # General patches
    common = ['change-userdir.sh', 'spack-derived-Allwmake']
    assets = []

    build_script  = './spack-derived-Allwmake'
    build_userdir = 'spack-userdir'  # Build user APPBIN, LIBBIN into here

    phases = ['configure', 'build', 'install']

    #
    # - End of definitions / setup -
    #

    def patch(self):
        """Copy additional files or other patching."""
        add_extra_files(self, self.common, self.assets)
        # Emit openfoam version immediately, if we resolved the wrong version
        # it takes a very long time to rebuild!
        tty.info('Build for ' + self.spec['openfoam'].format('$_$@$%@+$+'))

    def configure(self, spec, prefix):
        """Generate spack-config.sh file."""
        # Local tweaks
        # This is ugly, but otherwise it only looks for src/precice,
        # not the installed include files
        config = join_path(self.stage.source_path, 'spack-config.sh')
        with open(config, 'w') as out:
            out.write(
                """# Local tweaks for building
CPLUS_INCLUDE_PATH="{precice_dir}/include/precice${{CPLUS_INCLUDE_PATH:+:}}$CPLUS_INCLUDE_PATH"  ## noqa: E501
export CPLUS_INCLUDE_PATH
# Local build (for user appbin, libbin)
. ./change-userdir.sh $PWD/{user_dir}
#
"""
                .format(
                    precice_dir=spec['precice'].prefix,
                    user_dir=self.build_userdir))

    def build(self, spec, prefix):
        """Build with Allwmake script, wrapped to source environment first."""
        args = []
        if self.parallel:  # Parallel build? - pass via environment
            os.environ['WM_NCOMPPROCS'] = str(make_jobs)
        builder = Executable(self.build_script)
        builder(*args)

    def install(self, spec, prefix):
        """Install under the prefix directory"""

        for f in ['README.md', 'LICENSE']:
            if os.path.isfile(f):
                install(f, join_path(self.prefix, f))

        install_tree('tutorials', join_path(self.prefix, 'tutorials'))

        # Place directly under 'lib' (no bin)
        install_tree(
            join_path(self.build_userdir, 'lib'),
            join_path(self.prefix, 'lib'))
