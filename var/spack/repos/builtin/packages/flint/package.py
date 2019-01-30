# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

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
