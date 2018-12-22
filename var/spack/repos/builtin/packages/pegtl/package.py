# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack import *


# package has a Makefile, but only to build examples
class Pegtl(CMakePackage):
    """The Parsing Expression Grammar Template Library (PEGTL) is a
        zero-dependency C++11 header-only library for creating parsers
        according to a Parsing Expression Grammar (PEG).
    """

    homepage = "https://github.com/taocpp/PEGTL"
    url      = "https://github.com/taocpp/PEGTL/tarball/2.1.4"
    git      = "https://github.com/taocpp/PEGTL.git"

    version('develop', branch='master')
    version('2.1.4', 'e5288b6968e6e910287fce93dc5557bf')
    version('2.0.0', 'c772828e7188459338a920c21f9896db')
