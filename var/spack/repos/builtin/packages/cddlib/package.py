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
    version('0.94h', sha256='7382782c3834214b022c8b2898ed775a7bf915f2cb2acb73fa045d6fd9a3de33')

    # Note: It should be possible to build cddlib also without gmp

    depends_on("gmp")
    depends_on("libtool", type="build")

    def url_for_version(self, version):
        url = "https://github.com/cddlib/cddlib/archive/refs/tags/{0}.tar.gz"
        return url.format(version.dotted)
