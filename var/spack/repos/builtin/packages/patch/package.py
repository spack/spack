# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Patch(AutotoolsPackage):
    """Patch takes a patch file containing a difference listing produced by
    the diff program and applies those differences to one or more
    original files, producing patched versions.
    """

    homepage = "http://savannah.gnu.org/projects/patch/"
    url      = "https://ftpmirror.gnu.org/patch/patch-2.7.6.tar.xz"

    version('2.7.6', '78ad9937e4caadcba1526ef1853730d5')
    version('2.7.5', 'e3da7940431633fb65a01b91d3b7a27a')

    build_directory = 'spack-build'
