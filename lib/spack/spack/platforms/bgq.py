# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

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
