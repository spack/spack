##############################################################################
# Copyright (c) 2013-2016, Lawrence Livermore National Security, LLC.
# Produced at the Lawrence Livermore National Laboratory.
#
# This file is part of Spack.
# Created by Todd Gamblin, tgamblin@llnl.gov, All rights reserved.
# LLNL-CODE-647188
#
# For details, see https://github.com/llnl/spack
# Please also see the LICENSE file for our notice and the LGPL.
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
""" Test checks if the architecture class is created correctly and also that
    the functions are looking for the correct architecture name
"""
import itertools
import os
import platform as py_platform
import spack
import spack.architecture
from spack.spec import *
from spack.platforms.cray import Cray
from spack.platforms.linux import Linux
from spack.platforms.bgq import Bgq
from spack.platforms.darwin import Darwin

from spack.test.mock_packages_test import *


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

        new_arch = spack.architecture.Arch.from_dict(arch.to_dict())
        self.assertEqual(arch, new_arch)

        self.assertTrue(isinstance(arch, spack.architecture.Arch))
        self.assertTrue(isinstance(arch.platform, spack.architecture.Platform))
        self.assertTrue(isinstance(arch.platform_os,
                                   spack.architecture.OperatingSystem))
        self.assertTrue(isinstance(arch.target,
                                   spack.architecture.Target))
        self.assertTrue(isinstance(new_arch, spack.architecture.Arch))
        self.assertTrue(isinstance(new_arch.platform,
                                   spack.architecture.Platform))
        self.assertTrue(isinstance(new_arch.platform_os,
                                   spack.architecture.OperatingSystem))
        self.assertTrue(isinstance(new_arch.target,
                                   spack.architecture.Target))

    def test_platform(self):
        output_platform_class = spack.architecture.platform()
        if os.path.exists('/opt/cray/craype'):
            my_platform_class = Cray()
        elif os.path.exists('/bgsys'):
            my_platform_class = Bgq()
        elif 'Linux' in py_platform.system():
            my_platform_class = Linux()
        elif 'Darwin' in py_platform.system():
            my_platform_class = Darwin()

        self.assertEqual(str(output_platform_class), str(my_platform_class))

    def test_boolness(self):
        # Make sure architecture reports that it's False when nothing's set.
        arch = spack.architecture.Arch()
        self.assertFalse(arch)

        # Dummy architecture parts
        plat = spack.architecture.platform()
        plat_os = plat.operating_system('default_os')
        plat_target = plat.target('default_target')

        # Make sure architecture reports that it's True when anything is set.
        arch = spack.architecture.Arch()
        arch.platform = plat
        self.assertTrue(arch)

        arch = spack.architecture.Arch()
        arch.platform_os = plat_os
        self.assertTrue(arch)

        arch = spack.architecture.Arch()
        arch.target = plat_target
        self.assertTrue(arch)

    def test_user_front_end_input(self):
        """Test when user inputs just frontend that both the frontend target
            and frontend operating system match
        """
        frontend_os = str(self.platform.operating_system("frontend"))
        frontend_target = str(self.platform.target("frontend"))

        frontend_spec = Spec("libelf os=frontend target=frontend")
        frontend_spec.concretize()

        self.assertEqual(frontend_os, frontend_spec.architecture.platform_os)
        self.assertEqual(frontend_target, frontend_spec.architecture.target)

    def test_user_back_end_input(self):
        """Test when user inputs backend that both the backend target and
            backend operating system match
        """
        backend_os = str(self.platform.operating_system("backend"))
        backend_target = str(self.platform.target("backend"))

        backend_spec = Spec("libelf os=backend target=backend")
        backend_spec.concretize()

        self.assertEqual(backend_os, backend_spec.architecture.platform_os)
        self.assertEqual(backend_target, backend_spec.architecture.target)

    def test_user_defaults(self):
        default_os = str(self.platform.operating_system("default_os"))
        default_target = str(self.platform.target("default_target"))

        default_spec = Spec("libelf")  # default is no args
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
            o, t = arch
            spec = Spec("libelf os=%s target=%s" % (o, t))
            spec.concretize()
            results.append(spec.architecture.platform_os ==
                           str(self.platform.operating_system(o)))
            results.append(spec.architecture.target ==
                           str(self.platform.target(t)))
        res = all(results)

        self.assertTrue(res)
