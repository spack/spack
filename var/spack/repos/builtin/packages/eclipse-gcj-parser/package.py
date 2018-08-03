##############################################################################
# Copyright (c) 2013-2018, Lawrence Livermore National Security, LLC.
# Produced at the Lawrence Livermore National Laboratory.
#
# This file is part of Spack.
# Created by Todd Gamblin, tgamblin@llnl.gov, All rights reserved.
# LLNL-CODE-647188
#
# For details, see https://github.com/spack/spack
# Please also see the NOTICE and LICENSE files for our notice and the LGPL.
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
import os


class EclipseGcjParser(Package):
    """GCJ requires the Eclipse Java parser, but does not ship with it.
    This builds that parser into an executable binary, thereby
    making GCJ work."""

    homepage = "https://github.com/spack/spack/issues/8165"
    url = "ftp://sourceware.org/pub/java/ecj-4.8.jar"
    # Official download found at (see ecj-4.8M4.jar and ecjsrc-4.8M4.jar)
    # http://download.eclipse.org/eclipse/downloads/drops4/S-4.8M4-201712062000/

    maintainers = ['citibeth']

    version('4.8', 'd7cd6a27c8801e66cbaa964a039ecfdb', expand=False)

    phases = ('build', 'install')

    @property
    def gcj(self):
        """Obtain Executable for the gcj included with this GCC,
        even in the face of GCC binaries with version numbers
        included in their names."""

        dir, gcc = os.path.split(str(self.compiler.cc))
        if 'gcc' not in gcc:
            raise ValueError(
                'Package {0} requires GCC to build'.format(self.name))

        return Executable(join_path(dir, gcc.replace('gcc', 'gcj')))

    def build(self, spec, prefix):
        self.gcj(
            '-o', 'ecj1',
            '--main=org.eclipse.jdt.internal.compiler.batch.GCCMain',
            'ecj-4.8.jar')

    def install(self, spec, prefix):
        mkdirp(spec.prefix.bin)
        install('ecj1', spec.prefix.bin)

    def setup_environment(self, spack_env, run_env):
        run_env.prepend_path('PATH', self.prefix.bin)
