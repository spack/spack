# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack import *


class Heppdt(AutotoolsPackage):
    """The HepPID library contains translation methods for particle ID's
    to and from various Monte Carlo generators and the PDG standard
    numbering scheme. We realize that the generators adhere closely
    to the standard, but there are occasional differences."""
    homepage = "http://lcgapp.cern.ch/project/simu/HepPDT/"
    url      = "http://lcgapp.cern.ch/project/simu/HepPDT/download/HepPDT-2.06.01.tar.gz"

    version('3.04.01', 'a8e93c7603d844266b62d6f189f0ac7e')
    version('3.04.00', '2d2cd7552d3e9539148febacc6287db2')
    version('3.03.02', '0b85f1809bb8b0b28a46f23c718b2773')
    version('3.03.01', 'd411f3bfdf9c4350d802241ba2629cc2')
    version('3.03.00', 'cd84d0a0454be982dcd8c285e060a7b3')
    version('2.06.01', '5688b4bdbd84b48ed5dd2545a3dc33c0')
