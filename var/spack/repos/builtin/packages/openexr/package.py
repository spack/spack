# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Openexr(Package):
    """OpenEXR Graphics Tools (high dynamic-range image file format)"""

    homepage = "http://www.openexr.com/"
    url = "https://savannah.nongnu.org/download/openexr/openexr-2.2.0.tar.gz"

    version('2.2.0', 'b64e931c82aa3790329c21418373db4e')
    version('2.1.0', '33735d37d2ee01c6d8fbd0df94fb8b43')
    version('2.0.1', '4387e6050d2faa65dd5215618ff2ddce')
    version('1.7.0', '27113284f7d26a58f853c346e0851d7a')
    version('1.6.1', '11951f164f9c872b183df75e66de145a')
    version('1.5.0', '55342d2256ab3ae99da16f16b2e12ce9')
    version('1.4.0a', 'd0a4b9a930c766fa51561b05fb204afe')
    version('1.3.2', '1522fe69135016c52eb88fc7d8514409')

    variant('debug', default=False,
            description='Builds a debug version of the libraries')

    depends_on('pkgconfig', type='build')
    depends_on('ilmbase')

    def install(self, spec, prefix):
        configure_options = ['--prefix={0}'.format(prefix)]
        if '+debug' not in spec:
            configure_options.append('--disable-debug')
        configure(*configure_options)
        make('install')
