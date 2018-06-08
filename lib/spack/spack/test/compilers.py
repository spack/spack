##############################################################################
# Copyright (c) 2013-2018, Lawrence Livermore National Security, LLC.
# Produced at the Lawrence Livermore National Laboratory.
#
# This file is part of Spack.
# Created by Todd Gamblin, tgamblin@llnl.gov, All rights reserved.
# LLNL-CODE-647188
#
# For details, see https://github.com/spack/spack
# Please also see the NOTICE and LICENSE files for our notice and the LGPL.
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
from copy import copy
from six import iteritems

import spack.spec
import spack.compilers as compilers
from spack.compiler import _get_versioned_tuple, Compiler


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


def test_version_detection_is_empty():
    no_version = lambda x: None
    compiler_check_tuple = ('/usr/bin/gcc', '', r'\d\d', no_version)
    assert not _get_versioned_tuple(compiler_check_tuple)


def test_version_detection_is_successful():
    version = lambda x: '4.9'
    compiler_check_tuple = ('/usr/bin/gcc', '', r'\d\d', version)
    assert _get_versioned_tuple(compiler_check_tuple) == (
        '4.9', '', r'\d\d', '/usr/bin/gcc')


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

    compiler = compilers.compiler_from_config_entry(compiler_entry)
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


# Get the desired flag from the specified compiler spec.
def flag_value(flag, spec):
    compiler = None
    if spec is None:
        compiler = MockCompiler()
    else:
        compiler_entry = copy(default_compiler_entry)
        compiler_entry['spec'] = spec
        # Disable faulty id()-based cache (issue #7647).
        compilers._compiler_cache = {}
        compiler = compilers.compiler_from_config_entry(compiler_entry)

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
    unsupported_flag_test("openmp_flag", "clang@2.0.0-apple")
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
