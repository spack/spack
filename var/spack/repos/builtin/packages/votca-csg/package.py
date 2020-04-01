# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack import *


class VotcaCsg(CMakePackage):
    """Versatile Object-oriented Toolkit for Coarse-graining
       Applications (VOTCA) is a package intended to reduce the amount of
       routine work when doing systematic coarse-graining of various
       systems. The core is written in C++.

       This package contains the VOTCA coarse-graining engine.
    """
    homepage = "http://www.votca.org"
    url      = "https://github.com/votca/csg/tarball/v1.4"
    git      = "https://github.com/votca/csg.git"

    version('develop', branch='master')
    version('1.6_rc1', sha256='163701a65a34f90e8a850370167a82cbebf2b5c0774b7a8ad07884451fe9e332')
    version('1.5.1', sha256='7fca1261bd267bf38d2edd26259730fed3126c0c3fd91fb81940dbe17bb568fd', preferred=True)
    version('1.5', sha256='160387cdc51f87dd20ff2e2eed97086beee415d48f3c92f4199f6109068c8ff4')
    version('1.4.1', sha256='41dccaecadd0165c011bec36a113629e27745a5a133d1a042efe4356acdb5450')
    version('1.4', sha256='c13e7febd792de8c3d426203f089bd4d33b8067f9db5e8840e4579c88b61146e')

    depends_on("cmake@2.8:", type='build')
    for v in ["1.4", "1.4.1", "1.5", "1.5.1", "1.6_rc1", "develop"]:
        depends_on('votca-tools@%s' % v, when="@%s:%s.0" % (v, v))
    depends_on("boost")
    depends_on("gromacs~mpi@5.1:")
    depends_on("hdf5~mpi")
