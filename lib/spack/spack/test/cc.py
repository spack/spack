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
"""
This test checks that the Spack cc compiler wrapper is parsing
arguments correctly.
"""
import os
import pytest

from spack.paths import build_env_path
from spack.util.environment import system_dirs, set_env
from spack.util.executable import Executable

#
# Complicated compiler test command
#
test_args = [
    '-I/test/include', '-L/test/lib', '-L/other/lib', '-I/other/include',
    'arg1',
    '-Wl,--start-group',
    'arg2',
    '-Wl,-rpath,/first/rpath', 'arg3', '-Wl,-rpath', '-Wl,/second/rpath',
    '-llib1', '-llib2',
    'arg4',
    '-Wl,--end-group',
    '-Xlinker', '-rpath', '-Xlinker', '/third/rpath',
    '-Xlinker', '-rpath', '-Xlinker', '/fourth/rpath',
    '-llib3', '-llib4',
    'arg5', 'arg6']

#
# Pieces of the test command above, as they should be parsed out.
#
# `_wl_rpaths` are for the compiler (with -Wl,), and `_rpaths` are raw
# -rpath arguments for the linker.
#
test_include_paths = [
    '-I/test/include', '-I/other/include']

test_library_paths = [
    '-L/test/lib', '-L/other/lib']

test_wl_rpaths = [
    '-Wl,-rpath,/first/rpath', '-Wl,-rpath,/second/rpath',
    '-Wl,-rpath,/third/rpath', '-Wl,-rpath,/fourth/rpath']

test_rpaths = [
    '-rpath', '/first/rpath', '-rpath', '/second/rpath',
    '-rpath', '/third/rpath', '-rpath', '/fourth/rpath']

test_args_without_paths = [
    'arg1',
    '-Wl,--start-group',
    'arg2', 'arg3', '-llib1', '-llib2', 'arg4',
    '-Wl,--end-group',
    '-llib3', '-llib4', 'arg5', 'arg6']

#: The prefix of the package being mock installed
pkg_prefix = '/spack-test-prefix'

# Compilers to use during tests
cc = Executable(os.path.join(build_env_path, "cc"))
ld = Executable(os.path.join(build_env_path, "ld"))
cpp = Executable(os.path.join(build_env_path, "cpp"))
cxx = Executable(os.path.join(build_env_path, "c++"))
fc = Executable(os.path.join(build_env_path, "fc"))

#: the "real" compiler the wrapper is expected to invoke
real_cc = '/bin/mycc'

# mock flags to use in the wrapper environment
spack_cppflags = ['-g', '-O1', '-DVAR=VALUE']
spack_cflags   = ['-Wall']
spack_cxxflags = ['-Werror']
spack_fflags   = ['-w']
spack_ldflags  = ['-L', 'foo']
spack_ldlibs   = ['-lfoo']


@pytest.fixture(scope='session')
def wrapper_environment():
    with set_env(
            SPACK_CC=real_cc,
            SPACK_CXX=real_cc,
            SPACK_FC=real_cc,
            SPACK_PREFIX=pkg_prefix,
            SPACK_ENV_PATH='test',
            SPACK_DEBUG_LOG_DIR='.',
            SPACK_DEBUG_LOG_ID='foo-hashabc',
            SPACK_COMPILER_SPEC='gcc@4.4.7',
            SPACK_SHORT_SPEC='foo@1.2 arch=linux-rhel6-x86_64 /hashabc',
            SPACK_SYSTEM_DIRS=':'.join(system_dirs),
            SPACK_CC_RPATH_ARG='-Wl,-rpath,',
            SPACK_CXX_RPATH_ARG='-Wl,-rpath,',
            SPACK_F77_RPATH_ARG='-Wl,-rpath,',
            SPACK_FC_RPATH_ARG='-Wl,-rpath,',
            SPACK_DEPENDENCIES=None):
        yield


@pytest.fixture()
def wrapper_flags():
    with set_env(
            SPACK_CPPFLAGS=' '.join(spack_cppflags),
            SPACK_CFLAGS=' '.join(spack_cflags),
            SPACK_CXXFLAGS=' '.join(spack_cxxflags),
            SPACK_FFLAGS=' '.join(spack_fflags),
            SPACK_LDFLAGS=' '.join(spack_ldflags),
            SPACK_LDLIBS=' '.join(spack_ldlibs)):
        yield


class Dependencies(object):
    """
    dep1/
      include/
      lib/
    dep2/
      lib64/
    dep3/
      include/
      lib64/
    dep4/
      include/
    """
    def __init__(self):
        self.lib_dirs = list()
        self.link_args = list()
        self.rpath_dirs = list()
        self.ccld_rpath_args = list()
        self.ld_rpath_args = list()
        self.include_dirs = list()
        self.include_args = list()

    def add_lib(self, dep, rpath=True, dirname=None):
        prefix = 'dep{0}'.format(str(dep))
        dirname = dirname or 'lib'
        lib_dir = os.path.join(prefix, dirname)
        self.lib_dirs.append(lib_dir)
        self.link_args.append('-L' + lib_dir)
        if rpath:
            self.rpath_dirs.append(lib_dir)
            self.ccld_rpath_args.append('-Wl,-rpath,' + lib_dir)
            self.ld_rpath_args.append('' + lib_dir)

    def add_include(self, dep, dirname=None):
        prefix = 'dep{0}'.format(str(dep))
        dirname = dirname or 'include'
        include_dir = os.path.join(prefix, dirname)
        self.include_dirs.append(include_dir)
        self.include_args.append('-I' + include_dir)

    def spack_env_vars(self):
        return {
            'SPACK_INCLUDE_DIRS': ':'.join(self.include_dirs),
            'SPACK_LINK_DIRS': ':'.join(self.lib_dirs),
            'SPACK_RPATH_DIRS': ':'.join(self.rpath_dirs)
        }

pytestmark = pytest.mark.usefixtures('wrapper_environment')


def check_args(cc, args, expected):
    """Check output arguments that cc produces when called with args.

    This assumes that cc will print debug command output with one element
    per line, so that we see whether arguments that should (or shouldn't)
    contain spaces are parsed correctly.
    """
    with set_env(SPACK_TEST_COMMAND='dump-args'):
        cc_modified_args = cc(*args, output=str).strip().split('\n')
        assert expected == cc_modified_args


def dump_mode(cc, args):
    """Make cc dump the mode it detects, and return it."""
    with set_env(SPACK_TEST_COMMAND='dump-mode'):
        return cc(*args, output=str).strip()


def test_vcheck_mode():
    assert dump_mode(cc, ['-I/include', '--version']) == 'vcheck'
    assert dump_mode(cc, ['-I/include', '-V']) == 'vcheck'
    assert dump_mode(cc, ['-I/include', '-v']) == 'vcheck'
    assert dump_mode(cc, ['-I/include', '-dumpversion']) == 'vcheck'
    assert dump_mode(cc, ['-I/include', '--version', '-c']) == 'vcheck'
    assert dump_mode(cc, ['-I/include', '-V', '-o', 'output']) == 'vcheck'


def test_cpp_mode():
    assert dump_mode(cc, ['-E']) == 'cpp'
    assert dump_mode(cxx, ['-E']) == 'cpp'
    assert dump_mode(cpp, []) == 'cpp'


def test_as_mode():
    assert dump_mode(cc, ['-S']) == 'as'


def test_ccld_mode():
    assert dump_mode(cc, []) == 'ccld'
    assert dump_mode(cc, ['foo.c', '-o', 'foo']) == 'ccld'
    assert dump_mode(cc, ['foo.c', '-o', 'foo', '-Wl,-rpath,foo']) == 'ccld'
    assert dump_mode(cc, [
        'foo.o', 'bar.o', 'baz.o', '-o', 'foo', '-Wl,-rpath,foo']) == 'ccld'


def test_ld_mode():
    assert dump_mode(ld, []) == 'ld'
    assert dump_mode(ld, [
        'foo.o', 'bar.o', 'baz.o', '-o', 'foo', '-Wl,-rpath,foo']) == 'ld'


def test_ld_flags(wrapper_flags):
    check_args(
        ld, test_args,
        ['ld'] +
        spack_ldflags +
        test_include_paths +
        test_library_paths +
        test_rpaths +
        test_args_without_paths +
        spack_ldlibs)


def test_cpp_flags(wrapper_flags):
    check_args(
        cpp, test_args,
        ['cpp'] +
        spack_cppflags +
        test_include_paths +
        test_library_paths +
        test_args_without_paths)


def test_cc_flags(wrapper_flags):
    check_args(
        cc, test_args,
        [real_cc] +
        spack_cppflags +
        spack_cflags +
        spack_ldflags +
        test_include_paths +
        test_library_paths +
        test_wl_rpaths +
        test_args_without_paths +
        spack_ldlibs)


def test_cxx_flags(wrapper_flags):
    check_args(
        cxx, test_args,
        [real_cc] +
        spack_cppflags +
        spack_cxxflags +
        spack_ldflags +
        test_include_paths +
        test_library_paths +
        test_wl_rpaths +
        test_args_without_paths +
        spack_ldlibs)


def test_fc_flags(wrapper_flags):
    check_args(
        fc, test_args,
        [real_cc] +
        spack_fflags +
        spack_cppflags +
        spack_ldflags +
        test_include_paths +
        test_library_paths +
        test_wl_rpaths +
        test_args_without_paths +
        spack_ldlibs)


def test_dep_rpath():
    """Ensure RPATHs for root package are added."""
    check_args(
        cc, test_args,
        [real_cc] +
        test_include_paths +
        test_library_paths +
        test_wl_rpaths +
        test_args_without_paths)


def test_dep_include():
    """Ensure a single dependency include directory is added."""
    with set_env(SPACK_INCLUDE_DIRS='x'):
        check_args(
            cc, test_args,
            [real_cc] +
            test_include_paths +
            ['-Ix'] +
            test_library_paths +
            test_wl_rpaths +
            test_args_without_paths)


def test_dep_lib():
    """Ensure a single dependency RPATH is added."""
    with set_env(SPACK_LINK_DIRS='x',
                 SPACK_RPATH_DIRS='x'):
        check_args(
            cc, test_args,
            [real_cc] +
            test_include_paths +
            test_library_paths +
            ['-Lx'] +
            test_wl_rpaths +
            ['-Wl,-rpath,x'] +
            test_args_without_paths)


def test_dep_lib_no_rpath():
    """Ensure a single dependency link flag is added with no dep RPATH."""
    with set_env(SPACK_LINK_DIRS='x'):
        check_args(
            cc, test_args,
            [real_cc] +
            test_include_paths +
            test_library_paths +
            ['-Lx'] +
            test_wl_rpaths +
            test_args_without_paths)


def test_dep_lib_no_lib():
    """Ensure a single dependency RPATH is added with no -L."""
    with set_env(SPACK_RPATH_DIRS='x'):
        check_args(
            cc, test_args,
            [real_cc] +
            test_include_paths +
            test_library_paths +
            test_wl_rpaths +
            ['-Wl,-rpath,x'] +
            test_args_without_paths)


def test_ccld_deps():
    """Ensure all flags are added in ccld mode."""
    with set_env(SPACK_INCLUDE_DIRS='xinc:yinc:zinc',
                 SPACK_RPATH_DIRS='xlib:ylib:zlib',
                 SPACK_LINK_DIRS='xlib:ylib:zlib'):
        check_args(
            cc, test_args,
            [real_cc] +
            test_include_paths +
            ['-Ixinc',
             '-Iyinc',
             '-Izinc'] +
            test_library_paths +
            ['-Lxlib',
             '-Lylib',
             '-Lzlib'] +
            test_wl_rpaths +
            ['-Wl,-rpath,xlib',
             '-Wl,-rpath,ylib',
             '-Wl,-rpath,zlib'] +
            test_args_without_paths)


def test_cc_deps():
    """Ensure -L and RPATHs are not added in cc mode."""
    with set_env(SPACK_INCLUDE_DIRS='xinc:yinc:zinc',
                 SPACK_RPATH_DIRS='xlib:ylib:zlib',
                 SPACK_LINK_DIRS='xlib:ylib:zlib'):
        check_args(
            cc, ['-c'] + test_args,
            [real_cc] +
            test_include_paths +
            ['-Ixinc',
             '-Iyinc',
             '-Izinc'] +
            test_library_paths +
            ['-c'] +
            test_args_without_paths)


def test_ccld_with_system_dirs():
    """Ensure all flags are added in ccld mode."""
    with set_env(SPACK_INCLUDE_DIRS='xinc:yinc:zinc',
                 SPACK_RPATH_DIRS='xlib:ylib:zlib',
                 SPACK_LINK_DIRS='xlib:ylib:zlib'):

        sys_path_args = ['-I/usr/include',
                         '-L/usr/local/lib',
                         '-Wl,-rpath,/usr/lib64',
                         '-I/usr/local/include',
                         '-L/lib64/']
        check_args(
            cc, sys_path_args + test_args,
            [real_cc] +
            test_include_paths +
            ['-Ixinc',
             '-Iyinc',
             '-Izinc'] +
            ['-I/usr/include',
             '-I/usr/local/include'] +
            test_library_paths +
            ['-Lxlib',
             '-Lylib',
             '-Lzlib'] +
            ['-L/usr/local/lib',
             '-L/lib64/'] +
            test_wl_rpaths +
            ['-Wl,-rpath,xlib',
             '-Wl,-rpath,ylib',
             '-Wl,-rpath,zlib'] +
            ['-Wl,-rpath,/usr/lib64'] +
            test_args_without_paths)


def test_ld_deps():
    """Ensure no (extra) -I args or -Wl, are passed in ld mode."""
    with set_env(SPACK_INCLUDE_DIRS='xinc:yinc:zinc',
                 SPACK_RPATH_DIRS='xlib:ylib:zlib',
                 SPACK_LINK_DIRS='xlib:ylib:zlib'):
        check_args(
            ld, test_args,
            ['ld'] +
            test_include_paths +
            test_library_paths +
            ['-Lxlib',
             '-Lylib',
             '-Lzlib'] +
            test_rpaths +
            ['-rpath', 'xlib',
             '-rpath', 'ylib',
             '-rpath', 'zlib'] +
            test_args_without_paths)


def test_ld_deps_no_rpath():
    """Ensure SPACK_LINK_DEPS controls -L for ld."""
    with set_env(SPACK_INCLUDE_DIRS='xinc:yinc:zinc',
                 SPACK_LINK_DIRS='xlib:ylib:zlib'):
        check_args(
            ld, test_args,
            ['ld'] +
            test_include_paths +
            test_library_paths +
            ['-Lxlib',
             '-Lylib',
             '-Lzlib'] +
            test_rpaths +
            test_args_without_paths)


def test_ld_deps_no_link():
    """Ensure SPACK_RPATH_DEPS controls -rpath for ld."""
    with set_env(SPACK_INCLUDE_DIRS='xinc:yinc:zinc',
                 SPACK_RPATH_DIRS='xlib:ylib:zlib'):
        check_args(
            ld, test_args,
            ['ld'] +
            test_include_paths +
            test_library_paths +
            test_rpaths +
            ['-rpath', 'xlib',
             '-rpath', 'ylib',
             '-rpath', 'zlib'] +
            test_args_without_paths)


def test_ld_deps_partial():
    """Make sure ld -r (partial link) is handled correctly on OS's where it
       doesn't accept rpaths.
    """
    with set_env(SPACK_INCLUDE_DIRS='xinc',
                 SPACK_RPATH_DIRS='xlib',
                 SPACK_LINK_DIRS='xlib'):
        # TODO: do we need to add RPATHs on other platforms like Linux?
        # TODO: Can't we treat them the same?
        os.environ['SPACK_SHORT_SPEC'] = "foo@1.2=linux-x86_64"
        check_args(
            ld, ['-r'] + test_args,
            ['ld'] +
            test_include_paths +
            test_library_paths +
            ['-Lxlib'] +
            test_rpaths +
            ['-rpath', 'xlib'] +
            ['-r'] +
            test_args_without_paths)

        # rpaths from the underlying command will still appear
        # Spack will not add its own rpaths.
        os.environ['SPACK_SHORT_SPEC'] = "foo@1.2=darwin-x86_64"
        check_args(
            ld, ['-r'] + test_args,
            ['ld'] +
            test_include_paths +
            test_library_paths +
            ['-Lxlib'] +
            test_rpaths +
            ['-r'] +
            test_args_without_paths)


def test_ccache_prepend_for_cc():
    with set_env(SPACK_CCACHE_BINARY='ccache'):
        check_args(
            cc, test_args,
            ['ccache'] +  # ccache prepended in cc mode
            [real_cc] +
            test_include_paths +
            test_library_paths +
            test_wl_rpaths +
            test_args_without_paths)


def test_no_ccache_prepend_for_fc():
    check_args(
        fc, test_args,
        # no ccache for Fortran
        [real_cc] +
        test_include_paths +
        test_library_paths +
        test_wl_rpaths +
        test_args_without_paths)
