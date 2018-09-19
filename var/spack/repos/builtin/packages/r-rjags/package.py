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


class RRjags(RPackage):
    """Interface to the JAGS MCMC library.
       Usage: $ spack load r-rjags """

    homepage = "https://cran.r-project.org/web/packages/rjags/index.html"
    url      = "https://cran.r-project.org/src/contrib/rjags_4-6.tar.gz"

    version('4-6', 'c26b7cc8e8ddcdb55e14cba28df39f4c')

    depends_on('jags', type=('link'))
    depends_on('r-coda', type=('build', 'run'))

    def configure_args(self):
        args = ['--with-jags-lib=%s' % self.spec['jags'].prefix.lib,
                '--with-jags-include=%s' % self.spec['jags'].prefix.include,
                '--with-jags-modules=%s/JAGS/modules-4'
                % self.spec['jags'].prefix.lib]
        return args
