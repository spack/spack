# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack import *


class Hepmc(CMakePackage):
    """The HepMC package is an object oriented, C++ event record for
       High Energy Physics Monte Carlo generators and simulation."""

    homepage = "http://hepmc.web.cern.ch/hepmc/"
    url      = "http://hepmc.web.cern.ch/hepmc/releases/hepmc2.06.09.tgz"

    version('3.0.0',   '2212a5e8d693fbf726c28b43ebc6377a')
    version('2.06.09', '52518437a64f6b4284e9acc2ecad6212')
    version('2.06.08', 'a2e889114cafc4f60742029d69abd907')
    version('2.06.07', '11d7035dccb0650b331f51520c6172e7')
    version('2.06.06', '102e5503537a3ecd6ea6f466aa5bc4ae')
    version('2.06.05', '2a4a2a945adf26474b8bdccf4f881d9c')

    depends_on('cmake@2.6:', type='build')

    def cmake_args(self):
        return [
            '-Dmomentum:STRING=GEV',
            '-Dlength:STRING=MM',
        ]

    def url_for_version(self, version):
        if version <= Version("2.06.08"):
            url = "http://lcgapp.cern.ch/project/simu/HepMC/download/HepMC-{0}.tar.gz"
        else:
            url = "http://hepmc.web.cern.ch/hepmc/releases/hepmc{0}.tgz"
        return url.format(version)
