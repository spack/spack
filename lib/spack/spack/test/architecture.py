""" Test checks if the architecture class is created correctly and also that
    the functions are looking for the correct architecture name
"""
import unittest
import os
import platform
import spack
from spack.architecture import *
import spack.spec
from spack.platforms.cray_xc import CrayXc
from spack.platforms.linux import Linux
from spack.platforms.bgq import Bgq
from spack.platforms.darwin import Darwin

class ArchitectureTest(unittest.TestCase):
    
    def test_to_dict_function_with_architecture(self):
        arch = Arch()
        arch.platform_os = arch.platform.operating_system('default_os')
        arch.target = arch.platform.target('default')

        d = arch.to_dict()
        self.assertEqual(d, {'platform' : 'crayxc',
                             'platform_os' : {'name': 'CNL',
                                              'compiler_strategy' : 'MODULES',
                                              'version':'10'},
                             'target' : {'name': 'haswell',
                                         'module_name': 'craype-haswell'}})
                            
    def test_from_dict_function_with_architecture(self):
        d = {'platform':'crayxc',
             'platform_os' : {'name' : 'CNL', 'compiler_strategy': 'MODULES',
                                 'version': '10'},
             'target' : {'name':'haswell', 'module_name': 'craype-haswell'}}
                
        arch = spack.architecture.arch_from_dict(d)                                                
        self.assertTrue( isinstance(arch, Arch) )
        self.assertTrue( isinstance(arch.platform, Platform) )
        self.assertTrue( isinstance(arch.platform_os, OperatingSystem) )
        self.assertTrue( isinstance(arch.target, Target) )
        

    def test_platform_class_and_compiler_strategies(self):
        a = CrayXc()
        t = a.operating_system('default_os')
        self.assertEquals(t.compiler_strategy, 'MODULES')
        b = Linux()
        s = b.operating_system('default_os')
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
