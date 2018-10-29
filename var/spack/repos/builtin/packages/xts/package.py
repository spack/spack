# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Xts(AutotoolsPackage):
    """This is a revamped version of X Test Suite (XTS) which removes some of
    the ugliness of building and running the tests."""

    homepage = "https://www.x.org/wiki/XorgTesting/"
    url      = "https://www.x.org/archive/individual/test/xts-0.99.1.tar.gz"

    version('0.99.1', '1e5443fede389be606f3745a71483bac')

    depends_on('libx11')
    depends_on('libxext')
    depends_on('libxi')
    depends_on('libxtst')
    depends_on('libxau')
    depends_on('libxt')
    depends_on('libxmu')
    depends_on('libxaw')

    depends_on('xtrans', type='build')
    depends_on('bdftopcf', type='build')
    depends_on('mkfontdir', type='build')
    depends_on('perl', type='build')
    depends_on('xset', type='build')
    depends_on('xdpyinfo', type='build')

    # FIXME: Crashes during compilation
    # error: redeclaration of enumerator 'XawChainTop'
