# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack import *


class VotcaCsgTutorials(CMakePackage):
    """Versatile Object-oriented Toolkit for Coarse-graining
       Applications (VOTCA) is a package intended to reduce the amount of
       routine work when doing systematic coarse-graining of various
       systems. The core is written in C++.

       This package contains the VOTCA coarse-graining tutorials.
    """
    homepage = "http://www.votca.org"
    url      = "https://github.com/votca/csg-tutorials/tarball/v1.4"
    git      = "https://github.com/votca/csg-tutorials.git"

    version('develop', branch='master')
    version('1.6_rc1', sha256='87c4d945d2bdcb247e985cd407b0767c441f7810f1237ae65a63617f136e2ac9')
    version('1.5.1',   sha256='e35cea92df0e7d05ca7b449c1b5d84d887a3a23c7796abe3b84e4d6feec7faca', preferred=True)
    version('1.5',     sha256='03b841fb94129cf59781a7a5e3b71936c414aa9dfa17a50d7bc856d46274580c')
    version('1.4.1',   sha256='623724192c3a7d76b603a74a3326f181045f10f38b9f56dce754a90f1a74556e')
    version('1.4',     sha256='27d50acd68a9d8557fef18ec2b0c62841ae91c22275ab9afbd65c35e4dd5f719')

    for v in ["1.4", "1.4.1", "1.5", "1.5.1", "1.6_rc1", "develop"]:
        depends_on('votca-csg@%s' % v, when="@%s:%s.0" % (v, v))
    depends_on("boost")
