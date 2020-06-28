# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Random123(Package):
    """Random123 is a library of 'counter-based' random number
    generators (CBRNGs), in which the Nth random number can be obtained
    by applying a stateless mixing function to N instead of the
    conventional approach of using N iterations of a stateful
    transformation."""
    homepage = "http://www.deshawresearch.com/resources_random123.html"
    url      = "http://www.deshawresearch.com/downloads/download_random123.cgi/Random123-1.09.tar.gz"

    version('1.09', sha256='cf6abf623061bcf3d17e5e49bf3f3f0ae400ee89ae2e97c8cb8dcb918b1ebabe')

    patch('ibmxl.patch', when='@1.09')
    patch('arm-gcc.patch', when='@1.09')

    def install(self, spec, prefix):
        # Random123 doesn't have a build system.
        # We have to do our own install here.
        install_tree('include', prefix.include)
        install('./LICENSE', "%s" % prefix)
        # used by some packages, e.g. quinoa
        install('examples/uniform.hpp', join_path(prefix.include, 'Random123'))
