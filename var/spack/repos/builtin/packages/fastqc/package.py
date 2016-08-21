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
from distutils.dir_util import copy_tree


class Fastqc(Package):
    """A quality control tool for high throughput sequence data."""

    homepage = "http://www.bioinformatics.babraham.ac.uk/projects/fastqc/"
    url      = "http://www.bioinformatics.babraham.ac.uk/projects/fastqc/fastqc_v0.11.5.zip"

    version('0.11.5', '3524f101c0ab0bae77c7595983170a76')

    depends_on('jdk')
    depends_on('perl')          # for fastqc "script", any perl will do

    def install(self, spec, prefix):
        # ick...
        copy_tree('.', self.prefix)
        # ick, set_executable just makes it u+x, what about the others?
        chmod = which('chmod')
        chmod('+x', join_path(prefix, 'fastqc'))

    def setup_environment(self, spack_env, env):
        """Add <prefix> to the path; the package has a script at the
           top level."""

        env.prepend_path('PATH', self.prefix)
        env.prepend_path('PATH', join_path(self.spec['jdk'].prefix, 'bin'))
