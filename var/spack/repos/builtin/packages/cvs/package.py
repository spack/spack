# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack import *


class Cvs(AutotoolsPackage):
    """CVS a very traditional source control system"""
    homepage = "http://www.nongnu.org/cvs/"
    url      = "https://ftpmirror.gnu.org/non-gnu/cvs/source/feature/1.12.13/cvs-1.12.13.tar.bz2"

    version('1.12.13', '93a8dacc6ff0e723a130835713235863f1f5ada9')

    parallel = False
