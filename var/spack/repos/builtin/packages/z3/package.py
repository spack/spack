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


class Z3(MakefilePackage):
    """Z3 is a theorem prover from Microsoft Research.
    It is licensed under the MIT license."""

    homepage = "https://github.com/Z3Prover/z3/wiki"
    url      = "https://github.com/Z3Prover/z3/archive/z3-4.5.0.tar.gz"

    version('4.5.0', 'f332befa0d66d81818a06279a0973e25')
    version('4.4.1', '4336a9df24f090e711c6d42fd4e2b1fc')
    version('4.4.0', '2bcbb0381cc1572cace99aac8af08990')

    phases = ['bootstrap', 'build', 'install']

    variant('python', default=False, description='Enable python support')
    depends_on('python', when='+python')

    build_directory = 'build'

    def configure_args(self):
        spec = self.spec
        return [
            '--python' if '+python' in spec else ''
        ]

    def bootstrap(self, spec, prefix):
        options = ['--prefix={0}'.format(prefix)] + self.configure_args()
        spec['python'].command('scripts/mk_make.py', *options)
