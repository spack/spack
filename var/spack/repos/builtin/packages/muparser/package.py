# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Muparser(Package):
    """C++ math expression parser library."""
    homepage = "http://muparser.beltoforion.de/"
    url      = "https://github.com/beltoforion/muparser/archive/v2.2.5.tar.gz"

    version('2.2.5', '02dae671aa5ad955fdcbcd3fee313fb7')

    # Replace std::auto_ptr by std::unique_ptr
    # https://github.com/beltoforion/muparser/pull/46
    patch('auto_ptr.patch',
          when='@2.2.5')

    def install(self, spec, prefix):
        options = ['--disable-debug',
                   '--disable-dependency-tracking',
                   'CXXFLAGS=-std=c++11',
                   '--prefix=%s' % prefix]

        configure(*options)

        make(parallel=False)
        make("install")
