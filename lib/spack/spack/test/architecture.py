
# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

""" Test checks if the architecture class is created correctly and also that
    the functions are looking for the correct architecture name
"""
import os
import platform as py_platform

import pytest

import spack.architecture
from spack.spec import Spec
from spack.platforms.cray import Cray
from spack.platforms.linux import Linux
from spack.platforms.bgq import Bgq
from spack.platforms.darwin import Darwin


def test_dict_functions_for_architecture():
    arch = spack.architecture.Arch()
    arch.platform = spack.architecture.platform()
    arch.os = arch.platform.operating_system('default_os')
    arch.target = arch.platform.target('default_target')

    new_arch = spack.architecture.Arch.from_dict(arch.to_dict())

    assert arch == new_arch
    assert isinstance(arch, spack.architecture.Arch)
    assert isinstance(arch.platform, spack.architecture.Platform)
    assert isinstance(arch.os, spack.architecture.OperatingSystem)
    assert isinstance(arch.target, spack.architecture.Target)
    assert isinstance(new_arch, spack.architecture.Arch)
    assert isinstance(new_arch.platform, spack.architecture.Platform)
    assert isinstance(new_arch.os, spack.architecture.OperatingSystem)
    assert isinstance(new_arch.target, spack.architecture.Target)


def test_platform():
    output_platform_class = spack.architecture.real_platform()
    if os.environ.get('CRAYPE_VERSION') is not None:
        my_platform_class = Cray()
    elif os.path.exists('/bgsys'):
        my_platform_class = Bgq()
    elif 'Linux' in py_platform.system():
        my_platform_class = Linux()
    elif 'Darwin' in py_platform.system():
        my_platform_class = Darwin()

    assert str(output_platform_class) == str(my_platform_class)


def test_boolness():
    # Make sure architecture reports that it's False when nothing's set.
    arch = spack.architecture.Arch()
    assert not arch

    # Dummy architecture parts
    plat = spack.architecture.platform()
    plat_os = plat.operating_system('default_os')
    plat_target = plat.target('default_target')

    # Make sure architecture reports that it's True when anything is set.
    arch = spack.architecture.Arch()
    arch.platform = plat
    assert arch

    arch = spack.architecture.Arch()
    arch.os = plat_os
    assert arch

    arch = spack.architecture.Arch()
    arch.target = plat_target
    assert arch


def test_user_front_end_input(config):
    """Test when user inputs just frontend that both the frontend target
    and frontend operating system match
    """
    platform = spack.architecture.platform()
    frontend_os = str(platform.operating_system('frontend'))
    frontend_target = platform.target('frontend')

    frontend_spec = Spec('libelf os=frontend target=frontend')
    frontend_spec.concretize()

    assert frontend_os == frontend_spec.architecture.os
    assert frontend_target == frontend_spec.architecture.target


def test_user_back_end_input(config):
    """Test when user inputs backend that both the backend target and
    backend operating system match
    """
    platform = spack.architecture.platform()
    backend_os = str(platform.operating_system("backend"))
    backend_target = platform.target("backend")

    backend_spec = Spec("libelf os=backend target=backend")
    backend_spec.concretize()

    assert backend_os == backend_spec.architecture.os
    assert backend_target == backend_spec.architecture.target


def test_user_defaults(config):
    platform = spack.architecture.platform()
    default_os = str(platform.operating_system("default_os"))
    default_target = platform.target("default_target")

    default_spec = Spec("libelf")  # default is no args
    default_spec.concretize()

    assert default_os == default_spec.architecture.os
    assert default_target == default_spec.architecture.target


@pytest.mark.parametrize('operating_system', [
    x for x in spack.architecture.platform().operating_sys
] + ["fe", "be", "frontend", "backend"])
@pytest.mark.parametrize('target', [
    x for x in spack.architecture.platform().targets
] + ["fe", "be", "frontend", "backend"])
def test_user_input_combination(config, operating_system, target):
    platform = spack.architecture.platform()
    spec = Spec("libelf os=%s target=%s" % (operating_system, target))
    spec.concretize()
    assert spec.architecture.os == str(
        platform.operating_system(operating_system)
    )
    assert spec.architecture.target == platform.target(target)


def test_operating_system_conversion_to_dict():
    operating_system = spack.architecture.OperatingSystem('os', '1.0')
    assert operating_system.to_dict() == {
        'name': 'os', 'version': '1.0'
    }


@pytest.mark.parametrize('cpu_flag,target_name', [
    # Test that specific flags can be used in queries
    ('ssse3', 'haswell'),
    ('popcnt', 'nehalem'),
    ('avx512f', 'skylake_avx512'),
    ('avx512ifma', 'icelake'),
    # Test that proxy flags can be used in queries too
    ('sse3', 'nehalem'),
    ('avx512', 'skylake_avx512'),
    ('avx512', 'icelake'),
])
def test_target_container_semantic(cpu_flag, target_name):
    target = spack.architecture.Target(target_name)
    assert cpu_flag in target


@pytest.mark.parametrize('item,architecture_str', [
    # We can search the architecture string representation
    ('linux', 'linux-ubuntu18.04-haswell'),
    ('ubuntu', 'linux-ubuntu18.04-haswell'),
    ('haswell', 'linux-ubuntu18.04-haswell'),
    # We can also search flags of the target,
    ('avx512', 'linux-ubuntu18.04-icelake'),
])
def test_arch_spec_container_semantic(item, architecture_str):
    architecture = spack.spec.ArchSpec(architecture_str)
    assert item in architecture
