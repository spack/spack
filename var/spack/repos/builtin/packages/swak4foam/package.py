##############################################################################
# Copyright (c) 2017 Mark Olesen, OpenCFD Ltd.
#
# This file was authored by Mark Olesen <mark.olesen@esi-group.com>
# and is released as part of spack under the LGPL license.
# LLNL-CODE-647188
#
# For details, see https://github.com/llnl/spack
# Please also see the NOTICE and LICENSE files for the LLNL notice and LGPL.
#
# License
# -------
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
#
# Legal Notice
# ------------
# OPENFOAM is a trademark owned by OpenCFD Ltd
# (producer and distributor of the OpenFOAM software via www.openfoam.com).
# The trademark information must remain visible and unadulterated in this
# file and via the "spack info" and comply with the term set by
# http://openfoam.com/legal/trademark-policy.php
#
# This file is not part of OpenFOAM, nor does it constitute a component of an
# OpenFOAM distribution.
#
##############################################################################
#
# Notes
# - The build sometimes has problems with the parser:
#   >>>>
#       Parser library did not compile OK.
#       No sense continuing as everything else depends on it
#   >>>>
#
#   Just try building a second time and this complaint often disappears.
#
##############################################################################
from spack import *
from spack.environment import *
import llnl.util.tty as tty

import os
from spack.pkg.builtin.openfoam_com import add_extra_files


class Swak4foam(Package):
    """swak4foam (SWiss Army Knife for Foam) supplies additional libraries
    and utilities for OpenFOAM.
    This offering is not approved or endorsed by OpenCFD Ltd,
    producer and distributor of the OpenFOAM software via www.openfoam.com,
    and owner of the OPENFOAM trademark.
    """

    homepage = "https://openfoamwiki.net/index.php/Contrib/swak4Foam"
    gitrepo  = "https://github.com/Unofficial-Extend-Project-Mirror/openfoam-extend-swak4Foam-dev.git"
    hgrepo   = "http://hg.code.sf.net/p/openfoam-extend/swak4Foam"
    # The git mirror may be more convenient than hg (eg, shallow clone etc).

    version('develop', branch='branches/develop', git=gitrepo)

    variant('python', default=True, description='Build python modules')

    depends_on('openfoam+source')
    depends_on('python', when='+python')
    depends_on('flex', type='build')
    depends_on('bison@:2.7',  type='build')  # swak4Foam only tested with 2.x

    # General patches
    common = ['spack-derived-Allwmake', 'change-userdir.sh']
    assets = []

    build_script  = './spack-derived-Allwmake'  # <- Added by patch() method.
    build_userdir = 'spack-userdir'    # Build user APPBIN, LIBBIN into here
    config_file   = 'swakConfiguration'

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
        """Generate swakConfiguration and spack-config.sh file."""
        # Standard swakConfiguration file
        config = join_path(self.stage.source_path, self.config_file)
        with open(config, 'w') as out:
            if '+python' in spec:
                out.write(
                    """# With python
python_bin={python_bin}
python_config="$python_bin/python-config"
export SWAK_PYTHON_INCLUDE="$($python_config --cflags)"
export SWAK_PYTHON_LINK="$($python_config --ldflags)"

# Force python to be found first
PATH=$python_bin:$PATH
#
""".format(python_bin=spec['python'].prefix.bin))
            else:
                out.write('# No python requested\n')

        # Local tweaks
        config = join_path(self.stage.source_path, 'spack-config.sh')
        with open(config, 'w') as out:
            out.write(
                """# local tweaks for building
# Force bison to be found first
bison_bin={bison_bin}
PATH=$bison_bin:$PATH

# Local build (for user appbin, libbin)
[ -f change-userdir.sh ] && . ./change-userdir.sh $PWD/{user_dir}
#
"""
                .format(
                    bison_bin=spec['bison'].prefix.bin,
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

        # Retain swak config file
        for f in [self.config_file, 'COPYING']:
            if os.path.isfile(f):
                install(f, join_path(self.prefix, f))

        for d in ['Documentation', 'Examples']:
            install_tree(d, join_path(self.prefix, d))

        # Place these directly under 'bin' and 'lib'
        for d in ['bin', 'lib']:
            install_tree(
                join_path(self.build_userdir, d),
                join_path(self.prefix, d))
