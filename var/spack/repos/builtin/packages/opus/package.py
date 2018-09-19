##############################################################################
# Copyright (c) 2013-2018, Lawrence Livermore National Security, LLC.
# Produced at the Lawrence Livermore National Laboratory.
#
# This file is part of Spack.
# Created by Todd Gamblin, tgamblin@llnl.gov, All rights reserved.
# LLNL-CODE-647188
#
# For details, see https://github.com/spack/spack
# Please also see the NOTICE and LICENSE files for our notice and the LGPL.
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
from spack import *


class Opus(AutotoolsPackage):
    """Opus is a totally open, royalty-free, highly versatile audio codec."""

    homepage = "http://opus-codec.org/"
    url      = "http://downloads.xiph.org/releases/opus/opus-1.1.4.tar.gz"

    version('1.1.4',      'a2c09d995d0885665ff83b5df2505a5f')
    version('1.1.3',      '32bbb6b557fe1b6066adc0ae1f08b629')
    version('1.1.2',      '1f08a661bc72930187893a07f3741a91')
    version('1.1.1',      'cfb354d4c65217ca32a762f8ab15f2ac')
    version('1.1',        'c5a8cf7c0b066759542bc4ca46817ac6')
    version('1.0.3',      '86eedbd3c5a0171d2437850435e6edff')
    version('1.0.2',      'c503ad05a59ddb44deab96204401be03')
    version('1.0.1',      'bbac19996957b404a1139816e2f357f5')
    version('1.0.0',      'ec3ff0a16d9ad8c31a8856d13d97b155')
    version('0.9.14',     'c7161b247a8437ae6b0f11dd872e69e8')
    version('0.9.10',     'afbda2fd20dc08e6075db0f60297a137')
    version('0.9.9',      '0c18f0aac37f1ed955f5d694ddd88000')
    version('0.9.8',      '76c1876eae9169dee808ff4710d847cf')
    version('0.9.7',      '49834324ab618105cf112e161770b422')
    version('0.9.6',      '030556bcaebb241505f8577e92abe6d4')
    version('0.9.5',      '6bec090fd28996da0336e165b153ebd8')
    version('0.9.3',      '934226d4f572d01c5848bd70538248f5')
    version('0.9.2',      '8b9047956c4a781e05d3ac8565cd28f5')
    version('0.9.1',      'f58214e530928aa3db1dec217d5dfcd4')
    version('0.9.0',      '8a729db587430392e64280a499e9d061')

    depends_on('libvorbis')
