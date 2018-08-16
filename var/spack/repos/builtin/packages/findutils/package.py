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


class Findutils(AutotoolsPackage):
    """The GNU Find Utilities are the basic directory searching
       utilities of the GNU operating system."""

    homepage = "https://www.gnu.org/software/findutils/"
    url      = "https://ftpmirror.gnu.org/findutils/findutils-4.6.0.tar.gz"

    version('4.6.0',  '9936aa8009438ce185bea2694a997fc1')
    version('4.4.2',  '351cc4adb07d54877fa15f75fb77d39f')
    version('4.4.1',  '5883f569dc021eee765f330bb7a3782d')
    version('4.4.0',  '49e769ac4382fae6f104f99d54d0a112')
    version('4.2.33', 'b7e35aa175778c84942b1fee4144988b')
    version('4.2.32', 'aaa6beeb41a6f04963dff58f24a55b96')
    version('4.2.31', 'a0e31a0f18a49709bf5a449867c8049a')
    version('4.2.30', 'c35ff6502e0b3514c99089cb5d333c25')
    version('4.2.29', '24e76434ca74ba3c2c6ad621eb64e1ff')
    version('4.2.28', 'f5fb3349354ee3d94fceb81dab5c71fd')
    version('4.2.27', 'f1e0ddf09f28f8102ff3b90f3b5bc920')
    version('4.2.26', '9ac4e62937b1fdc4eb643d1d4bf117d3')
    version('4.2.25', 'e92fef6714ffa9972f28a1a423066921')
    version('4.2.23', 'ecaff8b060e8d69c10eb2391a8032e26')
    version('4.2.20', '7c8e12165b221dd67a19c00d780437a4')
    version('4.2.18', '8aac2498435f3f1882678fb9ebda5c34')
    version('4.2.15', 'a881b15aa7170aea045bf35cc92d48e7')
    version('4.1.20', 'e90ce7222daadeb8616b8db461e17cbc')
    version('4.1',    '3ea8fe58ef5386da75f6c707713aa059')
