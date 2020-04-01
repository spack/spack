# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack import *


class Cvs(AutotoolsPackage, GNUMirrorPackage):
    """CVS a very traditional source control system"""
    homepage = "http://www.nongnu.org/cvs/"
    gnu_mirror_path = "non-gnu/cvs/source/feature/1.12.13/cvs-1.12.13.tar.bz2"

    version('1.12.13', sha256='78853613b9a6873a30e1cc2417f738c330e75f887afdaf7b3d0800cb19ca515e')

    parallel = False
