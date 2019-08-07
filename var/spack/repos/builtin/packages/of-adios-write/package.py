# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

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
import os

import llnl.util.tty as tty

from spack import *
from spack.pkg.builtin.openfoam import add_extra_files


class OfAdiosWrite(Package):
    """adios-write supplies additional libraries and function objects
    for reading/writing OpenFOAM data with ADIOS.
    This offering is part of the community repository supported by OpenCFD Ltd,
    producer and distributor of the OpenFOAM software via www.openfoam.com,
    and owner of the OPENFOAM trademark.
    OpenCFD Ltd has been developing and releasing OpenFOAM since its debut
    in 2004.
    """

    # Currently only via git, but with some branches corresponding to main
    # OpenFOAM releases.
    homepage = "https://develop.openfoam.com/Community/feature-adiosWrite/"
    git      = "https://develop.openfoam.com/Community/feature-adiosWrite.git"

    version('develop', branch='develop')
    version('1706', branch='v1706')
    version('1612', branch='v1612')

    variant('source', default=True, description='Install library source')

    depends_on('openfoam@develop+source', when='@develop')
    depends_on('openfoam@1706+source', when='@1706')
    depends_on('openfoam@1612+source', when='@1612')
    depends_on('adios')

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
        tty.info('Build for ' + self.spec['openfoam'].format(
            '{name}{@version}{%compiler}{compiler_flags}{variants}'
        ))

    def configure(self, spec, prefix):
        """Generate spack-config.sh file."""
        # Local tweaks
        config = join_path(self.stage.source_path, 'spack-config.sh')
        with open(config, 'w') as out:
            out.write(
                """# Local tweaks for building
# Location of adios from spack
export ADIOS_ARCH_PATH={adios_dir}

# Local build (for user appbin, libbin)
. ./change-userdir.sh $PWD/{user_dir}
#
"""
                .format(
                    adios_dir=spec['adios'].prefix,
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

        for f in ['README.md', 'Issues.txt']:
            if os.path.isfile(f):
                install(f, join_path(self.prefix, f))

        dirs = ['doc', 'etc', 'tutorials']
        if '+source' in spec:
            dirs.append('src')

        for d in dirs:
            install_tree(d, join_path(self.prefix, d))

        # Place directly under 'lib' (no bin)
        for d in ['lib']:
            install_tree(
                join_path(self.build_userdir, d),
                join_path(self.prefix, d))
