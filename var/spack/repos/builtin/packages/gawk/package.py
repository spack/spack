# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Gawk(AutotoolsPackage):
    """If you are like many computer users, you would frequently like to make
       changes in various text files wherever certain patterns appear, or
       extract data from parts of certain lines while discarding the
       rest. To write a program to do this in a language such as C or
       Pascal is a time-consuming inconvenience that may take many lines
       of code. The job is easy with awk, especially the GNU
       implementation: gawk.

       The awk utility interprets a special-purpose programming language
       that makes it possible to handle simple data-reformatting jobs
       with just a few lines of code.
    """

    homepage = "https://www.gnu.org/software/gawk/"
    url      = "https://ftpmirror.gnu.org/gawk/gawk-4.1.4.tar.xz"

    version('4.1.4', '4e7dbc81163e60fd4f0b52496e7542c9')

    depends_on('gettext')
    depends_on('libsigsegv')
    depends_on('readline')
    depends_on('mpfr')
    depends_on('gmp')

    provides('awk')

    build_directory = 'spack-build'
