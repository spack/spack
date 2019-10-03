# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import pytest

import sys

from copy import copy
from six import iteritems

import spack.spec
import spack.compiler
import spack.compilers as compilers

import spack.compilers.arm
import spack.compilers.cce
import spack.compilers.clang
import spack.compilers.gcc
import spack.compilers.intel
import spack.compilers.nag
import spack.compilers.pgi
import spack.compilers.xl
import spack.compilers.xl_r
import spack.compilers.fj

from spack.compiler import Compiler


@pytest.fixture()
def make_args_for_version(monkeypatch):

    def _factory(version, path='/usr/bin/gcc'):
        class MockOs(object):
            pass

        compiler_name = 'gcc'
        compiler_cls = compilers.class_for_compiler_name(compiler_name)
        monkeypatch.setattr(compiler_cls, 'cc_version', lambda x: version)

        compiler_id = compilers.CompilerID(
            os=MockOs, compiler_name=compiler_name, version=None
        )
        variation = compilers.NameVariation(prefix='', suffix='')
        return compilers.DetectVersionArgs(
            id=compiler_id, variation=variation, language='cc', path=path
        )

    return _factory


def test_multiple_conflicting_compiler_definitions(mutable_config):
    compiler_def = {
        'compiler': {
            'flags': {},
            'modules': [],
            'paths': {
                'cc': 'cc',
                'cxx': 'cxx',
                'f77': 'null',
                'fc': 'null'},
            'extra_rpaths': [],
            'operating_system': 'test',
            'target': 'test',
            'environment': {},
            'spec': 'clang@0.0.0'}}

    compiler_config = [compiler_def, compiler_def]
    compiler_config[0]['compiler']['paths']['f77'] = 'f77'
    mutable_config.update_config('compilers', compiler_config)

    arch_spec = spack.spec.ArchSpec(('test', 'test', 'test'))
    cspec = compiler_config[0]['compiler']['spec']
    cmp = compilers.compiler_for_spec(cspec, arch_spec)
    assert cmp.f77 == 'f77'


def test_get_compiler_duplicates(config):
    # In this case there is only one instance of the specified compiler in
    # the test configuration (so it is not actually a duplicate), but the
    # method behaves the same.
    cfg_file_to_duplicates = compilers.get_compiler_duplicates(
        'gcc@4.5.0', spack.spec.ArchSpec('cray-CNL-xeon'))

    assert len(cfg_file_to_duplicates) == 1
    cfg_file, duplicates = next(iteritems(cfg_file_to_duplicates))
    assert len(duplicates) == 1


def test_all_compilers(config):
    all_compilers = compilers.all_compilers()
    filtered = [x for x in all_compilers if str(x.spec) == 'clang@3.3']
    filtered = [x for x in filtered if x.operating_system == 'SuSE11']
    assert len(filtered) == 1


@pytest.mark.skipif(
    sys.version_info[0] == 2, reason='make_args_for_version requires python 3'
)
@pytest.mark.parametrize('input_version,expected_version,expected_error', [
    (None, None,  "Couldn't get version for compiler /usr/bin/gcc"),
    ('4.9', '4.9', None)
])
def test_version_detection_is_empty(
        make_args_for_version, input_version, expected_version, expected_error
):
    args = make_args_for_version(version=input_version)
    result, error = compilers.detect_version(args)
    if not error:
        assert result.id.version == expected_version

    assert error == expected_error


def test_compiler_flags_from_config_are_grouped():
    compiler_entry = {
        'spec': 'intel@17.0.2',
        'operating_system': 'foo-os',
        'paths': {
            'cc': 'cc-path',
            'cxx': 'cxx-path',
            'fc': None,
            'f77': None
        },
        'flags': {
            'cflags': '-O0 -foo-flag foo-val'
        },
        'modules': None
    }

    compiler = compilers.compiler_from_dict(compiler_entry)
    assert any(x == '-foo-flag foo-val' for x in compiler.flags['cflags'])


# Test behavior of flags and UnsupportedCompilerFlag.

# Utility function to test most flags.
default_compiler_entry = {
    'spec': 'clang@2.0.0-apple',
    'operating_system': 'foo-os',
    'paths': {
        'cc': 'cc-path',
        'cxx': 'cxx-path',
        'fc': None,
        'f77': None
    },
    'flags': {},
    'modules': None
}


# Fake up a mock compiler where everything is defaulted.
class MockCompiler(Compiler):
    def __init__(self):
        super(MockCompiler, self).__init__(
            "badcompiler@1.0.0",
            default_compiler_entry['operating_system'],
            None,
            [default_compiler_entry['paths']['cc'],
             default_compiler_entry['paths']['cxx'],
             default_compiler_entry['paths']['fc'],
             default_compiler_entry['paths']['f77']])

    @property
    def name(self):
        return "mockcompiler"

    @property
    def version(self):
        return "1.0.0"

    required_libs = ['libgfortran']


def test_implicit_rpaths(dirs_with_libfiles, monkeypatch):
    lib_to_dirs, all_dirs = dirs_with_libfiles

    def try_all_dirs(*args):
        return all_dirs

    monkeypatch.setattr(MockCompiler, '_get_compiler_link_paths', try_all_dirs)

    expected_rpaths = set(lib_to_dirs['libstdc++'] +
                          lib_to_dirs['libgfortran'])

    compiler = MockCompiler()
    retrieved_rpaths = compiler.implicit_rpaths()
    assert set(retrieved_rpaths) == expected_rpaths


# Get the desired flag from the specified compiler spec.
def flag_value(flag, spec):
    compiler = None
    if spec is None:
        compiler = MockCompiler()
    else:
        compiler_entry = copy(default_compiler_entry)
        compiler_entry['spec'] = spec
        compiler = compilers.compiler_from_dict(compiler_entry)

    return getattr(compiler, flag)


# Utility function to verify that the expected exception is thrown for
# an unsupported flag.
def unsupported_flag_test(flag, spec=None):
    caught_exception = None
    try:
        flag_value(flag, spec)
    except spack.compiler.UnsupportedCompilerFlag:
        caught_exception = True

    assert(caught_exception and "Expected exception not thrown.")


# Verify the expected flag value for the give compiler spec.
def supported_flag_test(flag, flag_value_ref, spec=None):
    assert(flag_value(flag, spec) == flag_value_ref)


# Tests for UnsupportedCompilerFlag exceptions from default
# implementations of flags.
def test_default_flags():
    unsupported_flag_test("openmp_flag")
    unsupported_flag_test("cxx11_flag")
    unsupported_flag_test("cxx14_flag")
    unsupported_flag_test("cxx17_flag")
    supported_flag_test("cxx98_flag", "")


# Verify behavior of particular compiler definitions.
def test_clang_flags():
    # Common
    supported_flag_test("pic_flag", "-fPIC", "gcc@4.0")

    # Apple Clang.
    supported_flag_test(
        "openmp_flag", "-Xpreprocessor -fopenmp", "clang@2.0.0-apple")
    unsupported_flag_test("cxx11_flag", "clang@2.0.0-apple")
    supported_flag_test("cxx11_flag", "-std=c++11", "clang@4.0.0-apple")
    unsupported_flag_test("cxx14_flag", "clang@5.0.0-apple")
    supported_flag_test("cxx14_flag", "-std=c++1y", "clang@5.1.0-apple")
    supported_flag_test("cxx14_flag", "-std=c++14", "clang@6.1.0-apple")
    unsupported_flag_test("cxx17_flag", "clang@6.0.0-apple")
    supported_flag_test("cxx17_flag", "-std=c++1z", "clang@6.1.0-apple")

    # non-Apple Clang.
    supported_flag_test("openmp_flag", "-fopenmp", "clang@3.3")
    unsupported_flag_test("cxx11_flag", "clang@3.2")
    supported_flag_test("cxx11_flag", "-std=c++11", "clang@3.3")
    unsupported_flag_test("cxx14_flag", "clang@3.3")
    supported_flag_test("cxx14_flag", "-std=c++1y", "clang@3.4")
    supported_flag_test("cxx14_flag", "-std=c++14", "clang@3.5")
    unsupported_flag_test("cxx17_flag", "clang@3.4")
    supported_flag_test("cxx17_flag", "-std=c++1z", "clang@3.5")
    supported_flag_test("cxx17_flag", "-std=c++17", "clang@5.0")


def test_cce_flags():
    supported_flag_test("openmp_flag", "-h omp", "cce@1.0")
    supported_flag_test("cxx11_flag", "-h std=c++11", "cce@1.0")
    supported_flag_test("pic_flag", "-h PIC", "cce@1.0")


def test_gcc_flags():
    supported_flag_test("openmp_flag", "-fopenmp", "gcc@4.1")
    supported_flag_test("cxx98_flag", "", "gcc@5.2")
    supported_flag_test("cxx98_flag", "-std=c++98", "gcc@6.0")
    unsupported_flag_test("cxx11_flag", "gcc@4.2")
    supported_flag_test("cxx11_flag", "-std=c++0x", "gcc@4.3")
    supported_flag_test("cxx11_flag", "-std=c++11", "gcc@4.7")
    unsupported_flag_test("cxx14_flag", "gcc@4.7")
    supported_flag_test("cxx14_flag", "-std=c++1y", "gcc@4.8")
    supported_flag_test("cxx14_flag", "-std=c++14", "gcc@4.9")
    supported_flag_test("cxx14_flag", "", "gcc@6.0")
    unsupported_flag_test("cxx17_flag", "gcc@4.9")
    supported_flag_test("pic_flag", "-fPIC", "gcc@4.0")


def test_intel_flags():
    supported_flag_test("openmp_flag", "-openmp", "intel@15.0")
    supported_flag_test("openmp_flag", "-qopenmp", "intel@16.0")
    unsupported_flag_test("cxx11_flag", "intel@11.0")
    supported_flag_test("cxx11_flag", "-std=c++0x", "intel@12.0")
    supported_flag_test("cxx11_flag", "-std=c++11", "intel@13")
    unsupported_flag_test("cxx14_flag", "intel@14.0")
    supported_flag_test("cxx14_flag", "-std=c++1y", "intel@15.0")
    supported_flag_test("cxx14_flag", "-std=c++14", "intel@15.0.2")
    supported_flag_test("pic_flag", "-fPIC", "intel@1.0")


def test_nag_flags():
    supported_flag_test("openmp_flag", "-openmp", "nag@1.0")
    supported_flag_test("cxx11_flag", "-std=c++11", "nag@1.0")
    supported_flag_test("pic_flag", "-PIC", "nag@1.0")


def test_pgi_flags():
    supported_flag_test("openmp_flag", "-mp", "pgi@1.0")
    supported_flag_test("cxx11_flag", "-std=c++11", "pgi@1.0")
    supported_flag_test("pic_flag", "-fpic", "pgi@1.0")


def test_xl_flags():
    supported_flag_test("openmp_flag", "-qsmp=omp", "xl@1.0")
    unsupported_flag_test("cxx11_flag", "xl@13.0")
    supported_flag_test("cxx11_flag", "-qlanglvl=extended0x", "xl@13.1")
    supported_flag_test("pic_flag", "-qpic", "xl@1.0")


def test_xl_r_flags():
    supported_flag_test("openmp_flag", "-qsmp=omp", "xl_r@1.0")
    unsupported_flag_test("cxx11_flag", "xl_r@13.0")
    supported_flag_test("cxx11_flag", "-qlanglvl=extended0x", "xl_r@13.1")
    supported_flag_test("pic_flag", "-qpic", "xl_r@1.0")


def test_fj_flags():
    supported_flag_test("openmp_flag", "-Kopenmp", "fj@4.0.0")
    supported_flag_test("cxx98_flag", "-std=c++98", "fj@4.0.0")
    supported_flag_test("cxx11_flag", "-std=c++11", "fj@4.0.0")
    supported_flag_test("cxx14_flag", "-std=c++14", "fj@4.0.0")
    supported_flag_test("c99_flag", "-std=c99", "fj@4.0.0")
    supported_flag_test("c11_flag", "-std=c11", "fj@4.0.0")
    supported_flag_test("pic_flag", "-KPIC", "fj@4.0.0")


@pytest.mark.regression('10191')
@pytest.mark.parametrize('version_str,expected_version', [
    # macOS clang
    ('Apple clang version 11.0.0 (clang-1100.0.33.8)\n'
     'Target: x86_64-apple-darwin18.7.0\n'
     'Thread model: posix\n'
     'InstalledDir: /Applications/Xcode.app/Contents/Developer/Toolchains/XcodeDefault.xctoolchain/usr/bin\n',  # noqa
     '11.0.0-apple'),
    ('Apple LLVM version 7.0.2 (clang-700.1.81)\n'
     'Target: x86_64-apple-darwin15.2.0\n'
     'Thread model: posix\n', '7.0.2-apple'),
    # Other platforms
    ('clang version 6.0.1-svn334776-1~exp1~20181018152737.116 (branches/release_60)\n'  # noqa
     'Target: x86_64-pc-linux-gnu\n'
     'Thread model: posix\n'
     'InstalledDir: /usr/bin\n', '6.0.1'),
    ('clang version 3.1 (trunk 149096)\n'
     'Target: x86_64-unknown-linux-gnu\n'
     'Thread model: posix\n', '3.1'),
    ('clang version 8.0.0-3~ubuntu18.04.1 (tags/RELEASE_800/final)\n'
     'Target: x86_64-pc-linux-gnu\n'
     'Thread model: posix\n'
     'InstalledDir: /usr/bin\n', '8.0.0')
])
def test_clang_version_detection(version_str, expected_version):
    version = compilers.clang.Clang.extract_version_from_output(version_str)
    assert version == expected_version


@pytest.mark.parametrize('version_str,expected_version', [
    ('Arm C/C++/Fortran Compiler version 19.0 (build number 73) (based on LLVM 7.0.2)\n' # NOQA
     'Target: aarch64--linux-gnu\n'
     'Thread model: posix\n'
     'InstalledDir:\n'
     '/opt/arm/arm-hpc-compiler-19.0_Generic-AArch64_RHEL-7_aarch64-linux/bin\n', # NOQA
     '19.0')
])
def test_arm_version_detection(version_str, expected_version):
    version = spack.compilers.arm.Arm.extract_version_from_output(version_str)
    assert version == expected_version


@pytest.mark.parametrize('version_str,expected_version', [
    # Output of -dumpversion changed to return only major from GCC 7
    ('4.4.7\n', '4.4.7'),
    ('7\n', '7')
])
def test_gcc_version_detection(version_str, expected_version):
    version = spack.compilers.gcc.Gcc.extract_version_from_output(version_str)
    assert version == expected_version


@pytest.mark.parametrize('version_str,expected_version', [
    ('icpc (ICC) 12.1.5 20120612\n'
     'Copyright (C) 1985-2012 Intel Corporation.  All rights reserved.\n',
     '12.1.5'),
    ('ifort (IFORT) 12.1.5 20120612\n'
     'Copyright (C) 1985-2012 Intel Corporation.  All rights reserved.\n',
     '12.1.5')
])
def test_intel_version_detection(version_str, expected_version):
    version = compilers.intel.Intel.extract_version_from_output(version_str)
    assert version == expected_version


@pytest.mark.parametrize('version_str,expected_version', [
    ('NAG Fortran Compiler Release 6.0(Hibiya) Build 1037\n'
     'Product NPL6A60NA for x86-64 Linux\n', '6.0')
])
def test_nag_version_detection(version_str, expected_version):
    version = spack.compilers.nag.Nag.extract_version_from_output(version_str)
    assert version == expected_version


@pytest.mark.parametrize('version_str,expected_version', [
    # Output on x86-64
    ('pgcc 15.10-0 64-bit target on x86-64 Linux -tp sandybridge\n'
     'The Portland Group - PGI Compilers and Tools\n'
     'Copyright (c) 2015, NVIDIA CORPORATION.  All rights reserved.\n',
     '15.10'),
    # Output on PowerPC
    ('pgcc 17.4-0 linuxpower target on Linuxpower\n'
     'PGI Compilers and Tools\n'
     'Copyright (c) 2017, NVIDIA CORPORATION.  All rights reserved.\n',
     '17.4'),
    # Output when LLVM-enabled
    ('pgcc-llvm 18.4-0 LLVM 64-bit target on x86-64 Linux -tp haswell\n'
     'PGI Compilers and Tools\n'
     'Copyright (c) 2018, NVIDIA CORPORATION.  All rights reserved.\n',
     '18.4')
])
def test_pgi_version_detection(version_str, expected_version):
    version = spack.compilers.pgi.Pgi.extract_version_from_output(version_str)
    assert version == expected_version


@pytest.mark.parametrize('version_str,expected_version', [
    ('IBM XL C/C++ for Linux, V11.1 (5724-X14)\n'
     'Version: 11.01.0000.0000\n', '11.1'),
    ('IBM XL Fortran for Linux, V13.1 (5724-X16)\n'
     'Version: 13.01.0000.0000\n', '13.1'),
    ('IBM XL C/C++ for AIX, V11.1 (5724-X13)\n'
     'Version: 11.01.0000.0009\n', '11.1'),
    ('IBM XL C/C++ Advanced Edition for Blue Gene/P, V9.0\n'
     'Version: 09.00.0000.0017\n', '9.0')
])
def test_xl_version_detection(version_str, expected_version):
    version = spack.compilers.xl.Xl.extract_version_from_output(version_str)
    assert version == expected_version

    version = spack.compilers.xl_r.XlR.extract_version_from_output(version_str)
    assert version == expected_version


@pytest.mark.parametrize('version_str,expected_version', [
    ('Cray C : Version 8.4.6  Mon Apr 15, 2019  12:13:39\n', '8.4.6'),
    ('Cray C++ : Version 8.4.6  Mon Apr 15, 2019  12:13:45\n', '8.4.6'),
    ('Cray Fortran : Version 8.4.6  Mon Apr 15, 2019  12:13:55\n', '8.4.6')
])
def test_cce_version_detection(version_str, expected_version):
    version = spack.compilers.cce.Cce.extract_version_from_output(version_str)
    assert version == expected_version


@pytest.mark.parametrize('version_str,expected_version', [
    # C compiler
    ('fcc (FCC) 4.0.0 20190314\n'
     'simulating gcc version 6.1\n'
     'Copyright FUJITSU LIMITED 2019',
     '4.0.0'),
    # C++ compiler
    ('FCC (FCC) 4.0.0 20190314\n'
     'simulating gcc version 6.1\n'
     'Copyright FUJITSU LIMITED 2019',
     '4.0.0'),
    # Fortran compiler
    ('frt (FRT) 4.0.0 20190314\n'
     'Copyright FUJITSU LIMITED 2019',
     '4.0.0')
])
def test_fj_version_detection(version_str, expected_version):
    version = spack.compilers.fj.Fj.extract_version_from_output(version_str)
    assert version == expected_version
