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
import os
from spack.architecture import Platform, Target
from spack.operating_systems.linux_distro import LinuxDistro
from spack.operating_systems.cnk import Cnk


class Bgq(Platform):
    priority    = 30
    front_end   = 'power7'
    back_end    = 'ppc64'
    default     = 'ppc64'

    def __init__(self):
        ''' IBM Blue Gene/Q system platform.'''

        super(Bgq, self).__init__('bgq')

        self.add_target(self.front_end, Target(self.front_end))
        self.add_target(self.back_end, Target(self.back_end))

        front_distro = LinuxDistro()
        back_distro = Cnk()

        self.front_os = str(front_distro)
        self.back_os = str(back_distro)
        self.default_os = self.back_os

        self.add_operating_system(str(front_distro), front_distro)
        self.add_operating_system(str(back_distro), back_distro)

    @classmethod
    def detect(cls):
        return os.path.exists('/bgsys')
