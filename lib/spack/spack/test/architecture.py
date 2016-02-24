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
    
    def setUp(self):
        zlib = spack.spec.Spec("zlib")
        zlib.concretize()
        self.architecture = zlib.architecture
        self.platform = sys_type()
        self.platform_os = self.platform.operating_system('default_os')
        self.target = self.platform.target('default')

    #def test_to_dict_function_with_target(self):
    #    d = spack.architecture.to_dict(self.architecture)
    #    print d['target']
    #    self.assertEquals(d['target'], {'name': self.target.name,
    #                          'module_name' : self.target.module_name,
    #                          'platform_name' : self.target.platform_name,
    #                          'compiler_strategy': 'MODULES'
    #                          })

    def test_to_dict_function_with_architecture(self):
        d = spack.architecture.to_dict(self.architecture)
        self.assertEquals(d, {'architecture':
                                    {'platform' : {'name': 'crayxc'}, 
                                     'platform_os': {
                                                'compiler_strategy': 'MODULES', 
                                                 'name':'CNL', 
                                                 'version':'10'},
                                     'target' : {'platform_name' :'crayxc',
                                                 'module_name': 'craype-haswell',
                                                 'name':'haswell'}}})

    #def test_to_dict_function_with_operating_system(self):
    #    d = spack.architecture.to_dict(self.architecture)
    #    self.assertEquals(d['platform_os'], {'name': self.platform_os.name,
    #                          'version': self.platform_os.version,
    #                          'compiler_strategy': self.platform_os.compiler_strategy})

    def test_architecture_from_dict(self):
        pass

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
