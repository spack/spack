# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

# ----------------------------------------------------------------------------
# If you submit this package back to Spack as a pull request,
# please first remove this boilerplate and all FIXME comments.
#
# This is a template package file for Spack.  We've put "FIXME"
# next to all the things you'll want to change. Once you've handled
# them, you can save this file and test your package like this:
#
#     spack install rkt-cext-lib
#
# You can edit this file again by typing:
#
#     spack edit rkt-cext-lib
#
# See the Spack documentation for more information on packaging.
# ----------------------------------------------------------------------------

from spack import *


class RktCextLib(RacketPackage):
    """Racket library for running a C compiler/linker."""

    git      = "git@github.com:racket/cext-lib.git"

    maintainers = ['elfprince13']
    

    version('8.3', commit='cc22e2456df881a9008240d70dd9012ef37395f5') #tag = 'v8.3'

    depends_on('rkt-base@8.3', type=('build','run'), when='@8.3')
    depends_on('rkt-compiler-lib@8.3', type=('build','run'), when='@8.3')
    depends_on('rkt-dynext-lib@8.3', type=('build','run'), when='@8.3')
    depends_on('rkt-scheme-lib@8.3', type=('build','run'), when='@8.3')

    name = 'cext-lib'
    pkgs = True
    subdirectory = name
    
