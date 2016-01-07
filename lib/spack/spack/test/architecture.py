""" Test checks if the architecture class is created correctly and also that
    the functions are looking for the correct architecture name
"""
import unittest
import os
import platform
import spack
from spack.architecture import *
from spack.platforms.cray_xc import CrayXc
from spack.platforms.linux import Linux
from spack.platforms.bgq import Bgq
from spack.platforms.darwin import Darwin

class ArchitectureTest(unittest.TestCase):

    def test_platform_class_and_compiler_strategies(self):
        a = CrayXc()
        t = a.target('default')
        self.assertEquals(t.compiler_strategy, 'MODULES')
        b = Linux()
        s = b.target('default')
        self.assertEquals(s.compiler_strategy, 'PATH')

    def test_sys_type(self):
        output_platform_class = sys_type()
        my_arch_class = None
        if os.path.exists('/opt/cray/craype'):
            my_platform_class = CrayXc()
        elif os.path.exists('/bgsys'):
            my_platform_class = Bgq()
        elif 'Linux' in platform.system():
            my_platform_class = Linux()
        elif 'Darwin' in platform.system():
            my_platform_class = Darwin()

        self.assertEqual(str(output_platform_class), str(my_platform_class))
