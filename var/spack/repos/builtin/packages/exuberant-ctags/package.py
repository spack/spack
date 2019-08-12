# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class ExuberantCtags(AutotoolsPackage):
    """The canonical ctags generator"""
    homepage = "ctags.sourceforge.net"
    url      = "http://downloads.sourceforge.net/project/ctags/ctags/5.8/ctags-5.8.tar.gz"

    version('5.8', 'c00f82ecdcc357434731913e5b48630d')
