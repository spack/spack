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


class Flint(Package):
    """FLINT (Fast Library for Number Theory)."""

    homepage = "http://www.flintlib.org"
    url      = "http://mirrors.mit.edu/sage/spkg/upstream/flint/flint-2.5.2.tar.gz"
    git      = "https://github.com/wbhart/flint2.git"

    version('develop', branch='trunk')
    version('2.5.2', 'cda885309362150196aed66a5e0f0383')
    version('2.4.5', '6504b9deabeafb9313e57153a1730b33')

    # Overlap in functionality between gmp and mpir
    # All other dependencies must also be built with
    # one or the other
    # variant('mpir', default=False,
    #         description='Compile with the MPIR library')

    # Build dependencies
    depends_on('autoconf', type='build')

    # Other dependencies
    depends_on('gmp')   # mpir is a drop-in replacement for this
    depends_on('mpfr')  # Could also be built against mpir

    def install(self, spec, prefix):
        options = []
        options = ["--prefix=%s" % prefix,
                   "--with-gmp=%s" % spec['gmp'].prefix,
                   "--with-mpfr=%s" % spec['mpfr'].prefix]

        # if '+mpir' in spec:
        #     options.extend([
        #         "--with-mpir=%s" % spec['mpir'].prefix
        #     ])

        configure(*options)
        make()
        if self.run_tests:
            make("check")
        make("install")
