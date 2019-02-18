# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack import *


class VotcaCtp(CMakePackage):
    """Versatile Object-oriented Toolkit for Coarse-graining
       Applications (VOTCA) is a package intended to reduce the amount of
       routine work when doing systematic coarse-graining of various
       systems. The core is written in C++.

       This package contains the VOTCA charge transport engine.
    """
    homepage = "http://www.votca.org"
    url      = "https://github.com/votca/ctp/tarball/v1.5"
    git      = "https://github.com/votca/ctp.git"

    version('develop', branch='master')
    version('1.5', sha256='31eb6bcc9339e575116f0c91fe7a4ce7d4189f31f0640329c993fea911401d65')

    depends_on("cmake@2.8:", type='build')
    for v in ["1.5", "develop"]:
        depends_on('votca-tools@%s' % v, when="@%s" % v)
        depends_on('votca-csg@%s' % v, when="@%s" % v)
    depends_on("gsl")
