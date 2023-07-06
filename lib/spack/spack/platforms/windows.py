# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import platform

import archspec.cpu

import spack.target
from spack.operating_systems.windows_os import WindowsOs

from ._platform import Platform


class Windows(Platform):
    priority = 101

    def __init__(self):
        super().__init__("windows")

        for name in archspec.cpu.TARGETS:
            self.add_target(name, spack.target.Target(name))

        self.default = archspec.cpu.host().name
        self.front_end = self.default
        self.back_end = self.default

        windows_os = WindowsOs()

        self.default_os = str(windows_os)
        self.front_os = str(windows_os)
        self.back_os = str(windows_os)

        self.add_operating_system(str(windows_os), windows_os)

    @classmethod
    def detect(cls):
        plat = platform.system().lower()
        return "cygwin" in plat or "win32" in plat or "windows" in plat
