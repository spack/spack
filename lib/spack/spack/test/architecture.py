""" Test checks if the architecture class is created correctly and also that
    the functions are looking for the correct architecture name
"""
import unittest
import os
import platform as py_platform
import spack
import spack.architecture
from spack.spec import *
from spack.platforms.cray_xc import CrayXc
from spack.platforms.linux import Linux
from spack.platforms.bgq import Bgq
from spack.platforms.darwin import Darwin

from spack.test.mock_packages_test import *

#class ArchitectureTest(unittest.TestCase):
class ArchitectureTest(MockPackagesTest):

    def setUp(self):
        super(ArchitectureTest, self).setUp()
        self.platform = spack.architecture.platform()

    def tearDown(self):
        super(ArchitectureTest, self).tearDown()

    def test_dict_functions_for_architecture(self):
        arch = spack.architecture.Arch()
        arch.platform = spack.architecture.platform()
        arch.platform_os = arch.platform.operating_system('default_os')
        arch.target = arch.platform.target('default_target')

        d = arch.to_dict()

        new_arch = spack.architecture.arch_from_dict(d)

        self.assertEqual(arch, new_arch)

        self.assertTrue( isinstance(arch, spack.architecture.Arch) )
        self.assertTrue( isinstance(arch.platform, spack.architecture.Platform) )
        self.assertTrue( isinstance(arch.platform_os,
                                    spack.architecture.OperatingSystem) )
        self.assertTrue( isinstance(arch.target,
                                    spack.architecture.Target) )
        self.assertTrue( isinstance(new_arch, spack.architecture.Arch) )
        self.assertTrue( isinstance(new_arch.platform,
                                    spack.architecture.Platform) )
        self.assertTrue( isinstance(new_arch.platform_os,
                                    spack.architecture.OperatingSystem) )
        self.assertTrue( isinstance(new_arch.target,
                                    spack.architecture.Target) )


    def test_platform(self):
        output_platform_class = spack.architecture.platform()
        my_arch_class = None
        if os.path.exists('/opt/cray/craype'):
            my_platform_class = CrayXc()
        elif os.path.exists('/bgsys'):
            my_platform_class = Bgq()
        elif 'Linux' in py_platform.system():
            my_platform_class = Linux()
        elif 'Darwin' in py_platform.system():
            my_platform_class = Darwin()

        self.assertEqual(str(output_platform_class), str(my_platform_class))

    def test_user_front_end_input(self):
        """Test when user inputs just frontend that both the frontend target
            and frontend operating system match
        """
        frontend_os = self.platform.operating_system("frontend")
        frontend_target = self.platform.target("frontend")
        frontend_spec = Spec("libelf os=frontend target=frontend")
        frontend_spec.concretize()
        self.assertEqual(frontend_os, frontend_spec.architecture.platform_os)
        self.assertEqual(frontend_target, frontend_spec.architecture.target)

    def test_user_back_end_input(self):
        """Test when user inputs backend that both the backend target and
            backend operating system match
        """
        backend_os = self.platform.operating_system("backend")
        backend_target = self.platform.target("backend")
        backend_spec = Spec("libelf os=backend target=backend")
        backend_spec.concretize()
        self.assertEqual(backend_os, backend_spec.architecture.platform_os)
        self.assertEqual(backend_target, backend_spec.architecture.target)

    def test_user_defaults(self):
        default_os = self.platform.operating_system("default_os")
        default_target = self.platform.target("default_target")

        default_spec = Spec("libelf") # default is no args
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
            spec = Spec("libelf os=%s target=%s" % (o, t))
            spec.concretize()
            results.append(spec.architecture.platform_os == self.platform.operating_system(o))
            results.append(spec.architecture.target == self.platform.target(t))
        res = all(results)

        self.assertTrue(res)
