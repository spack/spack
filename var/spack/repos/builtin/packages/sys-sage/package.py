# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
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
#     spack install sys-sage
#
# You can edit this file again by typing:
#
#     spack edit sys-sage
#
# See the Spack documentation for more information on packaging.
# ----------------------------------------------------------------------------

from spack import *


class SysSage(CMakePackage):
    """A library for capturing hadrware topology and attributes of compute systems."""

    homepage = "https://github.com/stepanvanecek/sys-sage"
    url      = "https://github.com/stepanvanecek/sys-sage/archive/refs/tags/v0.1.1-alpha.tar.gz"
    git      = "https://github.com/stepanvanecek/sys-sage.git"

    # FIXME: Add a list of GitHub accounts to
    # notify when the package is updated.
    maintainers = ['stepanvanecek']

    version('master',  branch='master')
    version('0.1.1-alpha', sha256='441b5173e29cf69665518a5a5efb54342cc61b594a062c0b219f2cd1587442e1')

    # FIXME: Add dependencies if required.
    # depends_on('foo')
    depends_on('cmake@3.21:', type='build')
    depends_on('libxml2@2.9.13')
    #def cmake_args(self):
    #    # FIXME: Add arguments other than
    #    # FIXME: CMAKE_INSTALL_PREFIX and CMAKE_BUILD_TYPE
    #    # FIXME: If not needed delete this function
    #    args = []
    #    return args
