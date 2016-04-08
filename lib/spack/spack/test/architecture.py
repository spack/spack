""" Test checks if the architecture class is created correctly and also that
    the functions are looking for the correct architecture name
"""
import unittest
import os
import platform
import spack
from spack.architecture import *
from spack.spec import *
from spack.platforms.cray_xc import CrayXc
from spack.platforms.linux import Linux
from spack.platforms.bgq import Bgq
from spack.platforms.darwin import Darwin

class ArchitectureTest(unittest.TestCase):

    def test_dict_functions_for_architecture(self):
        arch = Arch()
        arch.platform_os = arch.platform.operating_system('default_os')
        arch.target = arch.platform.target('default_target')

        d = arch.to_dict()

        new_arch = spack.architecture.arch_from_dict(d)
        self.assertEqual(arch, new_arch)

        self.assertTrue( isinstance(arch, Arch) )
        self.assertTrue( isinstance(arch.platform, Platform) )
        self.assertTrue( isinstance(arch.platform_os, OperatingSystem) )
        self.assertTrue( isinstance(arch.target, Target) )
        self.assertTrue( isinstance(new_arch, Arch) )
        self.assertTrue( isinstance(new_arch.platform, Platform) )
        self.assertTrue( isinstance(new_arch.platform_os, OperatingSystem) )
        self.assertTrue( isinstance(new_arch.target, Target) )


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

    def setUp(self):
        self.platform = sys_type()

    def test_user_front_end_input(self):
        """Test when user inputs just frontend that both the frontend target
            and frontend operating system match
        """
        frontend_os = self.platform.operating_system("frontend")
        frontend_target = self.platform.target("frontend")
        frontend_spec = Spec("zlib=frontend")
        frontend_spec.concretize()
        self.assertEqual(frontend_os, frontend_spec.architecture.platform_os)
        self.assertEqual(frontend_target, frontend_spec.architecture.target)

    def test_user_back_end_input(self):
        """Test when user inputs backend that both the backend target and
            backend operating system match
        """
        backend_os = self.platform.operating_system("backend")
        backend_target = self.platform.target("backend")
        backend_spec = Spec("zlib=backend")
        backend_spec.concretize()
        self.assertEqual(backend_os, backend_spec.architecture.platform_os)
        self.assertEqual(backend_target, backend_spec.architecture.target)

    def test_user_defaults(self):
        default_os = self.platform.operating_system("default_os")
        default_target = self.platform.target("default_target")

        default_spec = Spec("zlib") # default is no args
        default_spec.concretize()
        self.assertEqual(default_os, default_spec.architecture.platform_os)
        self.assertEqual(default_target, default_spec.architecture.target)

    def test_user_input_combination(self):
        os_list = self.platform.operating_sys.keys()
        target_list = self.platform.targets.keys()  
        additional = ["fe", "be", "frontend", "backend"]

        os_list.extend(additional)
        target_list.extend(additional)  
        
        combinations = itertools.product(os_list, target_list)
        results = []
        for arch in combinations:
            o,t = arch
            arch_spec = "-".join(arch)
            spec = Spec("zlib=%s" % arch_spec)
            spec.concretize()
            results.append(spec.architecture.platform_os == self.platform.operating_system(o))
            results.append(spec.architecture.target == self.platform.target(t))
        res = all(results)
        print res
        self.assertTrue(res) 

