# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Fparser(CMakePackage):
    """This C++ library offers a class which can be used to parse and
    evaluate a mathematical function from a string (which might be eg
    requested from the user). The syntax of the function string is
    similar to mathematical expressions written in C/C++ (the exact
    syntax is specified in the documentation below). The function can
    then be evaluated with different values of variables."""

    homepage = "http://warp.povusers.org/FunctionParser/"
    git      = "https://github.com/thliebig/fparser.git"

    maintainers = ['dorton21']

    version('2015-09-25', commit='a59e1f51e32096bfe2a0a2640d5dffc7ae6ba37b')

    depends_on('cmake@2.8.0:', type='build')
