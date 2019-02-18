# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
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
    version('1.5', sha256='160387cdc51f87dd20ff2e2eed97086beee415d48f3c92f4199f6109068c8ff4')
    version('1.4.1', 'e4195d69db2036e9d76f22115ae31f81')
    version('1.4', 'd009e761e5e3afd51eed89c420610a67')

    depends_on("cmake@2.8:", type='build')
    for v in ["1.4", "1.4.1", "1.5", "develop"]:
        depends_on('votca-tools@%s' % v, when="@%s" % v)
    depends_on("gromacs~mpi@5.1:")
    depends_on("hdf5~mpi")
