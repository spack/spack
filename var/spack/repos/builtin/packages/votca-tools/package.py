# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack import *


class VotcaTools(CMakePackage):
    """Versatile Object-oriented Toolkit for Coarse-graining
       Applications (VOTCA) is a package intended to reduce the amount of
       routine work when doing systematic coarse-graining of various
       systems. The core is written in C++.

       This package contains the basic tools library of VOTCA.
    """
    homepage = "http://www.votca.org"
    url      = "https://github.com/votca/tools/tarball/v1.4"
    git      = "https://github.com/votca/tools.git"

    version('develop', branch='master')
    version('1.5', sha256='a82a6596c24ff06e79eab17ca02f4405745ceeeb66369693a59023ad0b62cf22')
    version('1.4.1', sha256='b6b87f6bec8db641a1d8660422ca44919252a69494b32ba6c8c9ac986bae9a65')
    version('1.4', sha256='41638122e7e59852af61d391b4ab8c308fd2e16652f768077e13a99d206ec5d3')

    depends_on("cmake@2.8:", type='build')
    depends_on("expat")
    depends_on("fftw")
    depends_on("gsl", when="@:1.4.9999")
    depends_on("eigen@3.3:", when="@1.5:")
    depends_on("boost")
    depends_on("sqlite")

    def cmake_args(self):
        args = [
            '-DWITH_RC_FILES=OFF'
        ]
        return args
