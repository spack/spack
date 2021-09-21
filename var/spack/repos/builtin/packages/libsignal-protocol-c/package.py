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
#     spack install libsignal-protocol-c
#
# You can edit this file again by typing:
#
#     spack edit libsignal-protocol-c
#
# See the Spack documentation for more information on packaging.
# ----------------------------------------------------------------------------

from spack import *


class LibsignalProtocolC(CMakePackage):
    """C library for the Signal protocol"""

    homepage = "https://signal.org/en/"
    url      = "https://github.com/signalapp/libsignal-protocol-c/archive/refs/tags/v2.3.3.tar.gz"

    maintainers = ['pwablito']

    version('2.3.3', sha256='c22e7690546e24d46210ca92dd808f17c3102e1344cd2f9a370136a96d22319d')


    def cmake_args(self):
        args = []
        return args
