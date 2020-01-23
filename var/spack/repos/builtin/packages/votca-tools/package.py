# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
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
    version('1.6_rc1', sha256='59b4bb64a93786a693e0cbc743a27c0bc451b9db2b0f63e4d2866f7aba10c268')
    version('1.5.1', sha256='4be4fe25a2910e24e1720cd9022d214001d38196033ade8f9d6e618b4f47d5c4', preferred=True)
    version('1.5', sha256='a82a6596c24ff06e79eab17ca02f4405745ceeeb66369693a59023ad0b62cf22')
    version('1.4.1', sha256='b6b87f6bec8db641a1d8660422ca44919252a69494b32ba6c8c9ac986bae9a65')
    version('1.4', sha256='41638122e7e59852af61d391b4ab8c308fd2e16652f768077e13a99d206ec5d3')

    # https://github.com/votca/tools/pull/197, fix cmake module
    patch("https://github.com/votca/tools/pull/197.patch", sha256="a06cce2a9cee63c8d01e4d1833f9cd2ba817b846c86fdb51ea5c9cd843135e68", when="@1.6_rc1")

    depends_on("cmake@2.8:", type='build')
    depends_on("expat")
    depends_on("fftw")
    depends_on("gsl", when="@:1.4.9999")
    depends_on("eigen@3.3:", when="@1.5:")
    depends_on("boost")
    depends_on("sqlite", when="@:1.5.9999")

    def cmake_args(self):
        args = [
            '-DWITH_RC_FILES=OFF'
        ]
        return args
