# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack import *


class Cddlib(AutotoolsPackage):
    """The C-library cddlib is a C implementation of the Double Description
    Method of Motzkin et al. for generating all vertices (i.e. extreme points)
    and extreme rays of a general convex polyhedron in R^d given by a system
    of linear inequalities"""

    homepage = "https://people.inf.ethz.ch/fukudak/cdd_home"
    url      = "https://github.com/cddlib/cddlib/archive/refs/tags/0.94h.tar.gz"
    maintainers = ['NessieCanCode']
    version('0.94m', sha256='70dffdb3369b8704dc75428a1b3c42ab9047b81ce039f12f427e2eb2b1b0dee2')
    version('0.94l', sha256='1ef6b1ee44509a26d480cda699ca1a9a38ecc9a2aba5092dbd7390ca285769e0')
    version('0.94k', sha256='de7397d7fe32758a6b53453a889ec7619b6c68a15d84eb132421f3d7d457be44')
    version('0.94j', sha256='27d7fcac2710755a01ef5381010140fc57c95f959c3c5705c58539d8c4d17bfb')
    version('0.94i', sha256='c60dac8697357740c593f8f255d49ac8a5069623561d68720fd9089367c90f4a')
    version('0.94h', sha256='7382782c3834214b022c8b2898ed775a7bf915f2cb2acb73fa045d6fd9a3de33')

    # Note: It should be possible to build cddlib also without gmp

    depends_on("gmp")
    depends_on("libtool", type="build")

    def url_for_version(self, version):
        if self.spec.satisfies('@:0.94i'):
            url = "https://github.com/cddlib/cddlib/archive/refs/tags/{0}.tar.gz"
        elif self.spec.satisfies('@0.94j:'):
            url = "https://github.com/cddlib/cddlib/releases/download/{0}/cddlib-{0}.tar.gz"
        return url.format(version.dotted)
