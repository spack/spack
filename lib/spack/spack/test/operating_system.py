""" Test checks if the operating_system class is created correctly and that
the functions are using the correct operating_system. Also checks whether
the operating_system correctly uses the compiler_strategy
"""

import unittest
import os
import platform
from spack.platforms.cray_xc import CrayXc
from spack.platforms.linux import Linux
from spack.platforms.darwin import Darwin
from spack.operating_system.linux_distro import LinuxDistro
from spack.operating_system.mac_os import MacOs
from spack.operating_system.cnl import ComputeNodeLinux

class TestOperatingSystem(unittest.TestCase):

    def setUp(self):
        cray_xc = CrayXc()
        linux   = Linux()
        darwin  = Darwin()
        self.cray_operating_sys = cray_xc.operating_system('front_os')
        self.cray_default_os = cray_xc.operating_system('default_os')
        self.cray_back_os = cray_xc.operating_system('back_os')
        self.darwin_operating_sys = darwin.operating_system('default_os')
        self.linux_operating_sys  = linux.operating_system('default_os')

    def test_cray_front_end_operating_system(self):
        self.assertIsInstance(self.cray_operating_sys, LinuxDistro)

    def test_cray_front_end_compiler_strategy(self):
        self.assertEquals(self.cray_operating_sys.compiler_strategy, "PATH")

    def test_cray_back_end_operating_system(self):
        self.assertIsInstance(self.cray_back_os,ComputeNodeLinux)

    def test_cray_back_end_compiler_strategy(self):
        self.assertEquals(self.cray_back_os.compiler_strategy, "MODULES")

    def test_linux_operating_system(self):
        self.assertIsInstance(self.linux_operating_sys, LinuxDistro)

    def test_linux_compiler_strategy(self):
        self.assertEquals(self.linux_operating_sys.compiler_strategy, "PATH")


    def test_cray_front_end_compiler_list(self):
        """ Operating systems will now be in charge of finding compilers.
            So, depending on which operating system you want to build for
            or which operating system you are on, then you could detect
            compilers in a certain way. Cray linux environment on the front
            end is just a regular linux distro whereas the Cray linux compute
            node is a stripped down version which modules are important
        """
        self.assertEquals(True, False)
