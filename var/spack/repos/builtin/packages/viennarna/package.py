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


class Viennarna(AutotoolsPackage):
    """The ViennaRNA Package consists of a C code library and several
    stand-alone programs for the prediction and comparison of RNA secondary
    structures.
    """

    homepage = "https://www.tbi.univie.ac.at/RNA/"
    url      = "https://www.tbi.univie.ac.at/RNA/download/sourcecode/2_4_x/ViennaRNA-2.4.3.tar.gz"

    version('2.4.3', '41be2fd36a5323a35ed50debfc7bd118')
    version('2.3.5', '4542120adae9b7abb605e2304c2a1326')

    variant('sse', default=True, description='Enable SSE in order to substantially speed up execution')
    variant('perl', default=True, description='Build ViennaRNA with Perl interface')
    variant('python', default=True, description='Build ViennaRNA with Python interface')

    depends_on('perl', type=('build', 'run'))
    depends_on('python', type=('build', 'run'))
    depends_on('libsvm')
    depends_on('gsl')

    def url_for_version(self, version):
        url = 'https://www.tbi.univie.ac.at/RNA/download/sourcecode/{0}_x/ViennaRNA-{1}.tar.gz'
        return url.format(version.up_to(2).underscored, version)

    def configure_args(self):

        args = self.enable_or_disable('sse')
        args += self.with_or_without('python')
        args += self.with_or_without('perl')
        if self.spec.satisfies('@2.4.3:'):
            args.append('--without-swig')

        if 'python@3:' in self.spec:
            args.append('--with-python3')

        return args
