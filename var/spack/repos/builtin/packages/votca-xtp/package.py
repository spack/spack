# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack import *


class VotcaXtp(CMakePackage):
    """Versatile Object-oriented Toolkit for Coarse-graining
       Applications (VOTCA) is a package intended to reduce the amount of
       routine work when doing systematic coarse-graining of various
       systems. The core is written in C++.

       This package contains the VOTCA exciton transport engine.
    """
    homepage = "http://www.votca.org"
    url      = "https://github.com/votca/xtp/tarball/v1.4.1"
    git      = "https://github.com/votca/xtp.git"

    version('develop', branch='master')
    version('1.6_rc1', sha256='144e74a6c4d31e490ca2bfaf4a30df12ccdc303efa5a7d1177c9b80035365ad5')
    version('1.5.1', sha256='17a7722e5a32d236e4f1f6f88b680da4ba5f52bcf65bca3687c6a1c731d10881', preferred=True)
    version('1.5', sha256='b40b6d19e13f0650e84b8beebe86ce5c09071624f18d66df826f9d8584b4d3c8')
    version('1.4.1', sha256='4b53d371d6cf648c9e9e9bd1f104d349cafeaf10a02866e3f1d05c574b595a21')

    depends_on("cmake@2.8:", type='build')
    for v in ["1.4.1", "1.5", "1.5.1", "1.6_rc1", "develop"]:
        depends_on('votca-tools@%s' % v, when="@%s:%s.0" % (v, v))
        depends_on('votca-csg@%s' % v, when="@%s:%s.0" % (v, v))
    depends_on("libxc", when='@1.5:')
    depends_on("ceres-solver", when='@1.5:1.5.9999')
    depends_on("hdf5+cxx~mpi")
