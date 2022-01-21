# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
import platform

import spack.operating_systems
import spack.target

from ._platform import Platform


class Test(Platform):
    priority    = 1000000

    if platform.system().lower() == 'darwin':
        binary_formats = ['macho']

    front_end = 'x86_64'
    back_end = 'core2'
    default = 'core2'

    front_os = 'redhat6'
    back_os = 'debian6'
    default_os = 'debian6'

    def __init__(self):
        super(Test, self).__init__('test')
        self.add_target(self.default, spack.target.Target(self.default))
        self.add_target(self.front_end, spack.target.Target(self.front_end))

        self.add_operating_system(
            self.default_os, spack.operating_systems.OperatingSystem('debian', 6))
        self.add_operating_system(
            self.front_os, spack.operating_systems.OperatingSystem('redhat', 6))

    @classmethod
    def detect(cls):
        return True
