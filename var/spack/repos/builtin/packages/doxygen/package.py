# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Doxygen(CMakePackage):
    """Doxygen is the de facto standard tool for generating documentation
    from annotated C++ sources, but it also supports other popular programming
    languages such as C, Objective-C, C#, PHP, Java, Python, IDL (Corba,
    Microsoft, and UNO/OpenOffice flavors), Fortran, VHDL, Tcl, and to some
    extent D.."""

    homepage = "http://www.stack.nl/~dimitri/doxygen/"
    url      = "http://ftp.stack.nl/pub/users/dimitri/doxygen-1.8.10.src.tar.gz"

    version('1.8.14', '41d8821133e8d8104280030553e2b42b')
    version('1.8.12', '08e0f7850c4d22cb5188da226b209a96')
    version('1.8.11', 'f4697a444feaed739cfa2f0644abc19b')
    version('1.8.10', '79767ccd986f12a0f949015efb5f058f')

    # graphviz appears to be a run-time optional dependency
    variant('graphviz', default=False,
            description='Build with dot command support from Graphviz.')

    depends_on("cmake@2.8.12:", type='build')
    depends_on("flex", type='build')
    depends_on("bison", type='build')

    # optional dependencies
    depends_on("graphviz", when="+graphviz", type='run')

    # Support C++14's std::shared_ptr. For details about this patch, see
    # https://github.com/Sleepyowl/doxygen/commit/6c380ba91ae41c6d5c409a5163119318932ae2a3?diff=unified
    # Also - https://github.com/doxygen/doxygen/pull/6588
    patch('shared_ptr.patch', when='@1.8.14')
