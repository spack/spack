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


class RBiocgenerics(Package):
    """S4 generic functions needed by many Bioconductor packages."""

    homepage = 'https://bioconductor.org/packages/BiocGenerics/'
    version('bioc-3.3',
            git='https://github.com/Bioconductor-mirror/BiocGenerics.git',
            branch='release-3.3')
    version('bioc-3.2',
            git='https://github.com/Bioconductor-mirror/BiocGenerics.git',
            branch='release-3.2')

    extends('R')

    def validate(self, spec):
        """
        Checks that the version of R is appropriate for the Bioconductor
        version.
        """
        if spec.satisfies('@bioc-3.3'):
            if not spec.satisfies('^R@3.3.0:3.3.9'):
                raise InstallError('Must use R-3.3 for Bioconductor-3.3')
        elif spec.satisfies('@bioc-3.2'):
            if not spec.satisfies('^R@3.2.0:3.2.9'):
                raise InstallError('Must use R-3.2 for Bioconductor-3.2')

    def install(self, spec, prefix):
        self.validate(spec)
        R('CMD', 'INSTALL', '--library=%s' %
          self.module.r_lib_dir, '%s' % self.stage.source_path)
