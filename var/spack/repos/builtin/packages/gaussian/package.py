##############################################################################
# Copyright (c) 2013-2016, Lawrence Livermore National Security, LLC.
# Produced at the Lawrence Livermore National Laboratory.
#
# This file is part of Spack.
# Created by Todd Gamblin, tgamblin@llnl.gov, All rights reserved.
# LLNL-CODE-647188
#
# For details, see https://github.com/llnl/spack
# Please also see the LICENSE file for our notice and the LGPL.
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

import distutils.dir_util


class Gaussian(Package):
    """Gaussian is a licensed software without a short description
    in the homepage.
    """

    homepage = "http://www.gaussian.com"

    version(
        'g09-D.01',
        '8730898096867217fef086386f643b4c',
        url="file:///home/ddossant/software/gaussian/g09-D.01.tar.gz"
    )

    def install(self, spec, prefix):
        distutils.dir_util.copy_tree(".", prefix + '/g09')

    def setup_environment(self, spack_env, run_env):

        prefix = self.prefix
        g09_dir = join_path(prefix, 'g09')

        run_env.set('g09root', self.prefix)

        exec_dirs = [
            g09_dir,
            join_path(g09_dir, 'bsd'),
            join_path(g09_dir, 'local')
        ]

        run_env.set('GAUSS_EXEDIR', ':'.join(exec_dirs))
        run_env.set('GAUSS_LEXEDIR', join_path(g09_dir, 'linda-exe'))
        run_env.set('GAUSS_ARCHDIR', join_path(g09_dir, 'arch'))
        run_env.set('GAUSS_BSDDIR', join_path(g09_dir, 'bsd'))
        run_env.prepend_path('PATH', ':'.join(exec_dirs))
        run_env.prepend_path('LD_LIBRARY_PATH', ':'.join(exec_dirs))
