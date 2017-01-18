##############################################################################
# Copyright (c) 2013-2016, Lawrence Livermore National Security, LLC.
# Produced at the Lawrence Livermore National Laboratory.
#
# This file is part of Spack.
# Created by Todd Gamblin, tgamblin@llnl.gov, All rights reserved.
# LLNL-CODE-647188
#
# For details, see https://github.com/llnl/spack
# Please also see the LICENSE file for our notice and the LGPL.
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License (as
# published by the Free Software Foundation) version 2.1, February 1999.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the IMPLIED WARRANTY OF
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the terms and
# conditions of the GNU Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public
# License along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA 02111-1307 USA
##############################################################################

import shutil
from spack import *


class Nauty(Package):
    """nauty and Traces are programs for computing automorphism groups of
    graphsq and digraphs"""
    homepage = "http://pallini.di.uniroma1.it/index.html"
    url      = "http://pallini.di.uniroma1.it/nauty26r7.tar.gz"

    version('2.6r7', 'b2b18e03ea7698db3fbe06c5d76ad8fe')
    version('2.6r5', '91b03a7b069962e94fc9aac8831ce8d2')
    version('2.5r9', 'e8ecd08b0892a1fb13329c147f08de6d')

    def url_for_version(self, version):
        url = "http://pallini.di.uniroma1.it/nauty{0}.tar.gz"
        return url.format(version.joined)

    def install(self, spec, prefix):
        configure('--prefix=%s' % prefix)
        make()

        exes = [
            "NRswitchg",
            "addedgeg",
            "amtog",
            "biplabg",
            "catg",
            "complg",
            "converseg",
            "copyg",
            "countg",
            "cubhamg",
            "deledgeg",
            "delptg",
            "directg",
            "dreadnaut",
            "dretodot",
            "dretog",
            "genbg",
            "genbgL",
            "geng",
            "genquarticg",
            "genrang",
            "genspecialg",
            "gentourng",
            "gentreeg",
            "hamheuristic",
            "labelg",
            "linegraphg",
            "listg",
            "multig",
            "newedgeg",
            "pickg",
            "planarg",
            "ranlabg",
            "shortg",
            "subdivideg",
            "twohamg",
            "vcolg",
            "watercluster2"]
        mkdirp(prefix.bin)
        for exe in exes:
            shutil.copyfile(exe, join_path(prefix.bin, exe))
