# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

"""
This test checks that the Spack cc compiler wrapper is parsing
arguments correctly.
"""
import os
import sys

import pytest

import spack.build_environment
import spack.config
import spack.spec
from spack.paths import build_env_path
from spack.util.environment import SYSTEM_DIRS, set_env
from spack.util.executable import Executable, ProcessError

#
# Complicated compiler test command
#
test_args = [
    "-I/test/include",
    "-L/test/lib",
    "-L/with space/lib",
    "-I/other/include",
    "arg1",
    "-Wl,--start-group",
    "arg2",
    "-Wl,-rpath,/first/rpath",
    "arg3",
    "-Wl,-rpath",
    "-Wl,/second/rpath",
    "-llib1",
    "-llib2",
    "arg4",
    "-Wl,--end-group",
    "-Xlinker",
    "-rpath",
    "-Xlinker",
    "/third/rpath",
    "-Xlinker",
    "-rpath",
    "-Xlinker",
    "/fourth/rpath",
    "-Wl,--rpath,/fifth/rpath",
    "-Wl,--rpath",
    "-Wl,/sixth/rpath",
    "-llib3",
    "-llib4",
    "arg5",
    "arg6",
    "-DGCC_ARG_WITH_PERENS=(A B C)",
    '"-DDOUBLE_QUOTED_ARG"',
    "'-DSINGLE_QUOTED_ARG'",
]

#
# Pieces of the test command above, as they should be parsed out.
#
# `_wl_rpaths` are for the compiler (with -Wl,), and `_rpaths` are raw
# -rpath arguments for the linker.
#
test_include_paths = ["-I/test/include", "-I/other/include"]

test_library_paths = ["-L/test/lib", "-L/with space/lib"]

test_wl_rpaths = [
    "-Wl,-rpath,/first/rpath",
    "-Wl,-rpath,/second/rpath",
    "-Wl,-rpath,/third/rpath",
    "-Wl,-rpath,/fourth/rpath",
    "-Wl,-rpath,/fifth/rpath",
    "-Wl,-rpath,/sixth/rpath",
]

test_rpaths = [
    "-rpath",
    "/first/rpath",
    "-rpath",
    "/second/rpath",
    "-rpath",
    "/third/rpath",
    "-rpath",
    "/fourth/rpath",
    "-rpath",
    "/fifth/rpath",
    "-rpath",
    "/sixth/rpath",
]

test_args_without_paths = [
    "arg1",
    "-Wl,--start-group",
    "arg2",
    "arg3",
    "-llib1",
    "-llib2",
    "arg4",
    "-Wl,--end-group",
    "-llib3",
    "-llib4",
    "arg5",
    "arg6",
    "-DGCC_ARG_WITH_PERENS=(A B C)",
    '"-DDOUBLE_QUOTED_ARG"',
    "'-DSINGLE_QUOTED_ARG'",
]

#: The prefix of the package being mock installed
pkg_prefix = "/spack-test-prefix"

# Compilers to use during tests
cc = Executable(os.path.join(build_env_path, "cc"))
ld = Executable(os.path.join(build_env_path, "ld"))
cpp = Executable(os.path.join(build_env_path, "cpp"))
cxx = Executable(os.path.join(build_env_path, "c++"))
fc = Executable(os.path.join(build_env_path, "fc"))

#: the "real" compiler the wrapper is expected to invoke
real_cc = "/bin/mycc"

# mock flags to use in the wrapper environment
spack_cppflags = ["-g", "-O1", "-DVAR=VALUE"]
spack_cflags = ["-Wall"]
spack_cxxflags = ["-Werror"]
spack_fflags = ["-w"]
spack_ldflags = ["-L", "foo"]
spack_ldlibs = ["-lfoo"]

lheaderpad = ["-Wl,-headerpad_max_install_names"]
headerpad = ["-headerpad_max_install_names"]

target_args = ["-march=znver2", "-mtune=znver2"]

# common compile arguments: includes, libs, -Wl linker args, other args
common_compile_args = (
    test_include_paths
    + test_library_paths
    + ["-Wl,--disable-new-dtags"]
    + test_wl_rpaths
    + test_args_without_paths
)

pytestmark = pytest.mark.skipif(sys.platform == "win32", reason="does not run on windows")


@pytest.fixture(scope="function")
def wrapper_environment(working_env):
    with set_env(
        SPACK_CC=real_cc,
        SPACK_CXX=real_cc,
        SPACK_FC=real_cc,
        SPACK_PREFIX=pkg_prefix,
        SPACK_ENV_PATH="test",
        SPACK_DEBUG_LOG_DIR=".",
        SPACK_DEBUG_LOG_ID="foo-hashabc",
        SPACK_COMPILER_SPEC="gcc@4.4.7",
        SPACK_SHORT_SPEC="foo@1.2 arch=linux-rhel6-x86_64 /hashabc",
        SPACK_SYSTEM_DIRS=":".join(SYSTEM_DIRS),
        SPACK_CC_RPATH_ARG="-Wl,-rpath,",
        SPACK_CXX_RPATH_ARG="-Wl,-rpath,",
        SPACK_F77_RPATH_ARG="-Wl,-rpath,",
        SPACK_FC_RPATH_ARG="-Wl,-rpath,",
        SPACK_LINK_DIRS=None,
        SPACK_INCLUDE_DIRS=None,
        SPACK_RPATH_DIRS=None,
        SPACK_TARGET_ARGS="-march=znver2 -mtune=znver2",
        SPACK_LINKER_ARG="-Wl,",
        SPACK_DTAGS_TO_ADD="--disable-new-dtags",
        SPACK_DTAGS_TO_STRIP="--enable-new-dtags",
        SPACK_COMPILER_FLAGS_KEEP="",
        SPACK_COMPILER_FLAGS_REPLACE="-Werror*",
    ):
        yield


@pytest.fixture()
def wrapper_flags():
    with set_env(
        SPACK_CPPFLAGS=" ".join(spack_cppflags),
        SPACK_CFLAGS=" ".join(spack_cflags),
        SPACK_CXXFLAGS=" ".join(spack_cxxflags),
        SPACK_FFLAGS=" ".join(spack_fflags),
        SPACK_LDFLAGS=" ".join(spack_ldflags),
        SPACK_LDLIBS=" ".join(spack_ldlibs),
    ):
        yield


def check_args(cc, args, expected):
    """Check output arguments that cc produces when called with args.

    This assumes that cc will print debug command output with one element
    per line, so that we see whether arguments that should (or shouldn't)
    contain spaces are parsed correctly.
    """
    with set_env(SPACK_TEST_COMMAND="dump-args"):
        cc_modified_args = cc(*args, output=str).strip().split("\n")
        assert expected == cc_modified_args


def check_args_contents(cc, args, must_contain, must_not_contain):
    """Check output arguments that cc produces when called with args.

    This assumes that cc will print debug command output with one element
    per line, so that we see whether arguments that should (or shouldn't)
    contain spaces are parsed correctly.
    """
    with set_env(SPACK_TEST_COMMAND="dump-args"):
        cc_modified_args = cc(*args, output=str).strip().split("\n")
        print(cc_modified_args)
        for a in must_contain:
            assert a in cc_modified_args
        for a in must_not_contain:
            assert a not in cc_modified_args


def check_env_var(executable, var, expected):
    """Check environment variables updated by the passed compiler wrapper

    This assumes that cc will print debug output when it's environment
    contains SPACK_TEST_COMMAND=dump-env-<variable-to-debug>
    """
    with set_env(SPACK_TEST_COMMAND="dump-env-" + var):
        output = executable(*test_args, output=str).strip()
        assert executable.path + ": " + var + ": " + expected == output


def dump_mode(cc, args):
    """Make cc dump the mode it detects, and return it."""
    with set_env(SPACK_TEST_COMMAND="dump-mode"):
        return cc(*args, output=str).strip()


def test_no_wrapper_environment():
    with pytest.raises(ProcessError):
        output = cc(output=str)
        assert "Spack compiler must be run from Spack" in output


def test_vcheck_mode(wrapper_environment):
    assert dump_mode(cc, ["-I/include", "--version"]) == "vcheck"
    assert dump_mode(cc, ["-I/include", "-V"]) == "vcheck"
    assert dump_mode(cc, ["-I/include", "-v"]) == "vcheck"
    assert dump_mode(cc, ["-I/include", "-dumpversion"]) == "vcheck"
    assert dump_mode(cc, ["-I/include", "--version", "-c"]) == "vcheck"
    assert dump_mode(cc, ["-I/include", "-V", "-o", "output"]) == "vcheck"


def test_cpp_mode(wrapper_environment):
    assert dump_mode(cc, ["-E"]) == "cpp"
    assert dump_mode(cxx, ["-E"]) == "cpp"
    assert dump_mode(cpp, []) == "cpp"


def test_as_mode(wrapper_environment):
    assert dump_mode(cc, ["-S"]) == "as"


def test_ccld_mode(wrapper_environment):
    assert dump_mode(cc, []) == "ccld"
    assert dump_mode(cc, ["foo.c", "-o", "foo"]) == "ccld"
    assert dump_mode(cc, ["foo.c", "-o", "foo", "-Wl,-rpath,foo"]) == "ccld"
    assert dump_mode(cc, ["foo.o", "bar.o", "baz.o", "-o", "foo", "-Wl,-rpath,foo"]) == "ccld"


def test_ld_mode(wrapper_environment):
    assert dump_mode(ld, []) == "ld"
    assert dump_mode(ld, ["foo.o", "bar.o", "baz.o", "-o", "foo", "-Wl,-rpath,foo"]) == "ld"


def test_ld_flags(wrapper_environment, wrapper_flags):
    check_args(
        ld,
        test_args,
        ["ld"]
        + spack_ldflags
        + test_include_paths
        + test_library_paths
        + ["--disable-new-dtags"]
        + test_rpaths
        + test_args_without_paths
        + spack_ldlibs,
    )


def test_cpp_flags(wrapper_environment, wrapper_flags):
    check_args(
        cpp,
        test_args,
        ["cpp"]
        + spack_cppflags
        + test_include_paths
        + test_library_paths
        + test_args_without_paths,
    )


def test_cc_flags(wrapper_environment, wrapper_flags):
    check_args(
        cc,
        test_args,
        [real_cc]
        + target_args
        + spack_cppflags
        + spack_cflags
        + spack_ldflags
        + common_compile_args
        + spack_ldlibs,
    )


def test_cxx_flags(wrapper_environment, wrapper_flags):
    check_args(
        cxx,
        test_args,
        [real_cc]
        + target_args
        + spack_cppflags
        + spack_cxxflags
        + spack_ldflags
        + common_compile_args
        + spack_ldlibs,
    )


def test_fc_flags(wrapper_environment, wrapper_flags):
    check_args(
        fc,
        test_args,
        [real_cc]
        + target_args
        + spack_fflags
        + spack_cppflags
        + spack_ldflags
        + common_compile_args
        + spack_ldlibs,
    )


def test_Wl_parsing(wrapper_environment):
    check_args(
        cc,
        ["-Wl,-rpath,/a,--enable-new-dtags,-rpath=/b,--rpath", "-Wl,/c"],
        [real_cc]
        + target_args
        + ["-Wl,--disable-new-dtags", "-Wl,-rpath,/a", "-Wl,-rpath,/b", "-Wl,-rpath,/c"],
    )


def test_dep_rpath(wrapper_environment):
    """Ensure RPATHs for root package are added."""
    check_args(cc, test_args, [real_cc] + target_args + common_compile_args)


def test_dep_include(wrapper_environment):
    """Ensure a single dependency include directory is added."""
    with set_env(SPACK_INCLUDE_DIRS="x"):
        check_args(
            cc,
            test_args,
            [real_cc]
            + target_args
            + test_include_paths
            + ["-Ix"]
            + test_library_paths
            + ["-Wl,--disable-new-dtags"]
            + test_wl_rpaths
            + test_args_without_paths,
        )


def test_system_path_cleanup(wrapper_environment):
    """Ensure SPACK_ENV_PATH is removed from PATH, even with trailing /

    The compiler wrapper has to ensure that it is not called nested
    like it would happen when gcc's collect2 looks in PATH for ld.

    To prevent nested calls, the compiler wrapper removes the elements
    of SPACK_ENV_PATH from PATH. Autotest's generated testsuite appends
    a / to each element of PATH when adding AUTOTEST_PATH.
    Thus, ensure that PATH cleanup works even with trailing /.
    """
    system_path = "/bin:/usr/bin:/usr/local/bin"
    cc_dir = os.path.dirname(cc.path)
    with set_env(SPACK_ENV_PATH=cc_dir, SPACK_CC="true"):
        with set_env(PATH=cc_dir + ":" + system_path):
            check_env_var(cc, "PATH", system_path)
        with set_env(PATH=cc_dir + "/:" + system_path):
            check_env_var(cc, "PATH", system_path)


def test_dep_lib(wrapper_environment):
    """Ensure a single dependency RPATH is added."""
    with set_env(SPACK_LINK_DIRS="x", SPACK_RPATH_DIRS="x"):
        check_args(
            cc,
            test_args,
            [real_cc]
            + target_args
            + test_include_paths
            + test_library_paths
            + ["-Lx"]
            + ["-Wl,--disable-new-dtags"]
            + test_wl_rpaths
            + ["-Wl,-rpath,x"]
            + test_args_without_paths,
        )


def test_dep_lib_no_rpath(wrapper_environment):
    """Ensure a single dependency link flag is added with no dep RPATH."""
    with set_env(SPACK_LINK_DIRS="x"):
        check_args(
            cc,
            test_args,
            [real_cc]
            + target_args
            + test_include_paths
            + test_library_paths
            + ["-Lx"]
            + ["-Wl,--disable-new-dtags"]
            + test_wl_rpaths
            + test_args_without_paths,
        )


def test_dep_lib_no_lib(wrapper_environment):
    """Ensure a single dependency RPATH is added with no -L."""
    with set_env(SPACK_RPATH_DIRS="x"):
        check_args(
            cc,
            test_args,
            [real_cc]
            + target_args
            + test_include_paths
            + test_library_paths
            + ["-Wl,--disable-new-dtags"]
            + test_wl_rpaths
            + ["-Wl,-rpath,x"]
            + test_args_without_paths,
        )


def test_ccld_deps(wrapper_environment):
    """Ensure all flags are added in ccld mode."""
    with set_env(
        SPACK_INCLUDE_DIRS="xinc:yinc:zinc",
        SPACK_RPATH_DIRS="xlib:ylib:zlib",
        SPACK_LINK_DIRS="xlib:ylib:zlib",
    ):
        check_args(
            cc,
            test_args,
            [real_cc]
            + target_args
            + test_include_paths
            + ["-Ixinc", "-Iyinc", "-Izinc"]
            + test_library_paths
            + ["-Lxlib", "-Lylib", "-Lzlib"]
            + ["-Wl,--disable-new-dtags"]
            + test_wl_rpaths
            + ["-Wl,-rpath,xlib", "-Wl,-rpath,ylib", "-Wl,-rpath,zlib"]
            + test_args_without_paths,
        )


def test_ccld_deps_isystem(wrapper_environment):
    """Ensure all flags are added in ccld mode.
    When a build uses -isystem, Spack should inject it's
    include paths using -isystem. Spack will insert these
    after any provided -isystem includes, but before any
    system directories included using -isystem"""
    with set_env(
        SPACK_INCLUDE_DIRS="xinc:yinc:zinc",
        SPACK_RPATH_DIRS="xlib:ylib:zlib",
        SPACK_LINK_DIRS="xlib:ylib:zlib",
    ):
        mytest_args = test_args + ["-isystem", "fooinc"]
        check_args(
            cc,
            mytest_args,
            [real_cc]
            + target_args
            + test_include_paths
            + ["-isystem", "fooinc", "-isystem", "xinc", "-isystem", "yinc", "-isystem", "zinc"]
            + test_library_paths
            + ["-Lxlib", "-Lylib", "-Lzlib"]
            + ["-Wl,--disable-new-dtags"]
            + test_wl_rpaths
            + ["-Wl,-rpath,xlib", "-Wl,-rpath,ylib", "-Wl,-rpath,zlib"]
            + test_args_without_paths,
        )


def test_cc_deps(wrapper_environment):
    """Ensure -L and RPATHs are not added in cc mode."""
    with set_env(
        SPACK_INCLUDE_DIRS="xinc:yinc:zinc",
        SPACK_RPATH_DIRS="xlib:ylib:zlib",
        SPACK_LINK_DIRS="xlib:ylib:zlib",
    ):
        check_args(
            cc,
            ["-c"] + test_args,
            [real_cc]
            + target_args
            + test_include_paths
            + ["-Ixinc", "-Iyinc", "-Izinc"]
            + test_library_paths
            + ["-c"]
            + test_args_without_paths,
        )


def test_ccld_with_system_dirs(wrapper_environment):
    """Ensure all flags are added in ccld mode."""
    with set_env(
        SPACK_INCLUDE_DIRS="xinc:yinc:zinc",
        SPACK_RPATH_DIRS="xlib:ylib:zlib",
        SPACK_LINK_DIRS="xlib:ylib:zlib",
    ):
        sys_path_args = [
            "-I/usr/include",
            "-L/usr/local/lib",
            "-Wl,-rpath,/usr/lib64",
            "-I/usr/local/include",
            "-L/lib64/",
        ]
        check_args(
            cc,
            sys_path_args + test_args,
            [real_cc]
            + target_args
            + test_include_paths
            + ["-Ixinc", "-Iyinc", "-Izinc"]
            + ["-I/usr/include", "-I/usr/local/include"]
            + test_library_paths
            + ["-Lxlib", "-Lylib", "-Lzlib"]
            + ["-L/usr/local/lib", "-L/lib64/"]
            + ["-Wl,--disable-new-dtags"]
            + test_wl_rpaths
            + ["-Wl,-rpath,xlib", "-Wl,-rpath,ylib", "-Wl,-rpath,zlib"]
            + ["-Wl,-rpath,/usr/lib64"]
            + test_args_without_paths,
        )


def test_ccld_with_system_dirs_isystem(wrapper_environment):
    """Ensure all flags are added in ccld mode.
    Ensure that includes are in the proper
    place when a build uses -isystem, and uses
    system directories in the include paths"""
    with set_env(
        SPACK_INCLUDE_DIRS="xinc:yinc:zinc",
        SPACK_RPATH_DIRS="xlib:ylib:zlib",
        SPACK_LINK_DIRS="xlib:ylib:zlib",
    ):
        sys_path_args = [
            "-isystem",
            "/usr/include",
            "-L/usr/local/lib",
            "-Wl,-rpath,/usr/lib64",
            "-isystem",
            "/usr/local/include",
            "-L/lib64/",
        ]
        check_args(
            cc,
            sys_path_args + test_args,
            [real_cc]
            + target_args
            + test_include_paths
            + ["-isystem", "xinc", "-isystem", "yinc", "-isystem", "zinc"]
            + ["-isystem", "/usr/include", "-isystem", "/usr/local/include"]
            + test_library_paths
            + ["-Lxlib", "-Lylib", "-Lzlib"]
            + ["-L/usr/local/lib", "-L/lib64/"]
            + ["-Wl,--disable-new-dtags"]
            + test_wl_rpaths
            + ["-Wl,-rpath,xlib", "-Wl,-rpath,ylib", "-Wl,-rpath,zlib"]
            + ["-Wl,-rpath,/usr/lib64"]
            + test_args_without_paths,
        )


def test_ld_deps(wrapper_environment):
    """Ensure no (extra) -I args or -Wl, are passed in ld mode."""
    with set_env(
        SPACK_INCLUDE_DIRS="xinc:yinc:zinc",
        SPACK_RPATH_DIRS="xlib:ylib:zlib",
        SPACK_LINK_DIRS="xlib:ylib:zlib",
    ):
        check_args(
            ld,
            test_args,
            ["ld"]
            + test_include_paths
            + test_library_paths
            + ["-Lxlib", "-Lylib", "-Lzlib"]
            + ["--disable-new-dtags"]
            + test_rpaths
            + ["-rpath", "xlib", "-rpath", "ylib", "-rpath", "zlib"]
            + test_args_without_paths,
        )


def test_ld_deps_no_rpath(wrapper_environment):
    """Ensure SPACK_LINK_DEPS controls -L for ld."""
    with set_env(SPACK_INCLUDE_DIRS="xinc:yinc:zinc", SPACK_LINK_DIRS="xlib:ylib:zlib"):
        check_args(
            ld,
            test_args,
            ["ld"]
            + test_include_paths
            + test_library_paths
            + ["-Lxlib", "-Lylib", "-Lzlib"]
            + ["--disable-new-dtags"]
            + test_rpaths
            + test_args_without_paths,
        )


def test_ld_deps_no_link(wrapper_environment):
    """Ensure SPACK_RPATH_DEPS controls -rpath for ld."""
    with set_env(SPACK_INCLUDE_DIRS="xinc:yinc:zinc", SPACK_RPATH_DIRS="xlib:ylib:zlib"):
        check_args(
            ld,
            test_args,
            ["ld"]
            + test_include_paths
            + test_library_paths
            + ["--disable-new-dtags"]
            + test_rpaths
            + ["-rpath", "xlib", "-rpath", "ylib", "-rpath", "zlib"]
            + test_args_without_paths,
        )


def test_ld_deps_partial(wrapper_environment):
    """Make sure ld -r (partial link) is handled correctly on OS's where it
    doesn't accept rpaths.
    """
    with set_env(SPACK_INCLUDE_DIRS="xinc", SPACK_RPATH_DIRS="xlib", SPACK_LINK_DIRS="xlib"):
        # TODO: do we need to add RPATHs on other platforms like Linux?
        # TODO: Can't we treat them the same?
        os.environ["SPACK_SHORT_SPEC"] = "foo@1.2=linux-x86_64"
        check_args(
            ld,
            ["-r"] + test_args,
            ["ld"]
            + test_include_paths
            + test_library_paths
            + ["-Lxlib"]
            + ["--disable-new-dtags"]
            + test_rpaths
            + ["-rpath", "xlib"]
            + ["-r"]
            + test_args_without_paths,
        )

        # rpaths from the underlying command will still appear
        # Spack will not add its own rpaths.
        os.environ["SPACK_SHORT_SPEC"] = "foo@1.2=darwin-x86_64"
        check_args(
            ld,
            ["-r"] + test_args,
            ["ld"]
            + headerpad
            + test_include_paths
            + test_library_paths
            + ["-Lxlib"]
            + ["--disable-new-dtags"]
            + test_rpaths
            + ["-r"]
            + test_args_without_paths,
        )


def test_ccache_prepend_for_cc(wrapper_environment):
    with set_env(SPACK_CCACHE_BINARY="ccache"):
        os.environ["SPACK_SHORT_SPEC"] = "foo@1.2=linux-x86_64"
        check_args(
            cc,
            test_args,
            ["ccache"]
            + [real_cc]  # ccache prepended in cc mode
            + target_args
            + common_compile_args,
        )
        os.environ["SPACK_SHORT_SPEC"] = "foo@1.2=darwin-x86_64"
        check_args(
            cc,
            test_args,
            ["ccache"]
            + [real_cc]  # ccache prepended in cc mode
            + target_args
            + lheaderpad
            + common_compile_args,
        )


def test_no_ccache_prepend_for_fc(wrapper_environment):
    os.environ["SPACK_SHORT_SPEC"] = "foo@1.2=linux-x86_64"
    check_args(
        fc,
        test_args,
        # no ccache for Fortran
        [real_cc] + target_args + common_compile_args,
    )
    os.environ["SPACK_SHORT_SPEC"] = "foo@1.2=darwin-x86_64"
    check_args(
        fc,
        test_args,
        # no ccache for Fortran
        [real_cc] + target_args + lheaderpad + common_compile_args,
    )


def test_keep_and_replace(wrapper_environment):
    werror_specific = ["-Werror=meh"]
    werror = ["-Werror"]
    werror_all = werror_specific + werror
    with set_env(SPACK_COMPILER_FLAGS_KEEP="", SPACK_COMPILER_FLAGS_REPLACE="-Werror*|"):
        check_args_contents(cc, test_args + werror_all, ["-Wl,--end-group"], werror_all)
    with set_env(SPACK_COMPILER_FLAGS_KEEP="-Werror=*", SPACK_COMPILER_FLAGS_REPLACE="-Werror*|"):
        check_args_contents(cc, test_args + werror_all, werror_specific, werror)
    with set_env(
        SPACK_COMPILER_FLAGS_KEEP="-Werror=*",
        SPACK_COMPILER_FLAGS_REPLACE="-Werror*| -llib1| -Wl*|",
    ):
        check_args_contents(
            cc, test_args + werror_all, werror_specific, werror + ["-llib1", "-Wl,--rpath"]
        )


@pytest.mark.parametrize(
    "cfg_override,initial,expected,must_be_gone",
    [
        # Set and unset variables
        (
            "config:flags:keep_werror:all",
            ["-Werror", "-Werror=specific", "-bah"],
            ["-Werror", "-Werror=specific", "-bah"],
            [],
        ),
        (
            "config:flags:keep_werror:specific",
            ["-Werror", "-Werror=specific", "-bah"],
            ["-Werror=specific", "-bah"],
            ["-Werror"],
        ),
        (
            "config:flags:keep_werror:none",
            ["-Werror", "-Werror=specific", "-bah"],
            ["-bah", "-Wno-error", "-Wno-error=specific"],
            ["-Werror", "-Werror=specific"],
        ),
        # check non-standard -Werror opts like -Werror-implicit-function-declaration
        (
            "config:flags:keep_werror:all",
            ["-Werror", "-Werror-implicit-function-declaration", "-bah"],
            ["-Werror", "-Werror-implicit-function-declaration", "-bah"],
            [],
        ),
        (
            "config:flags:keep_werror:specific",
            ["-Werror", "-Werror-implicit-function-declaration", "-bah"],
            ["-Werror-implicit-function-declaration", "-bah", "-Wno-error"],
            ["-Werror"],
        ),
        (
            "config:flags:keep_werror:none",
            ["-Werror", "-Werror-implicit-function-declaration", "-bah"],
            ["-bah", "-Wno-error=implicit-function-declaration"],
            ["-Werror", "-Werror-implicit-function-declaration"],
        ),
    ],
)
@pytest.mark.usefixtures("wrapper_environment", "mutable_config")
def test_flag_modification(cfg_override, initial, expected, must_be_gone):
    spack.config.add(cfg_override)
    env = spack.build_environment.clean_environment()

    keep_werror = spack.config.get("config:flags:keep_werror")
    spack.build_environment._add_werror_handling(keep_werror, env)
    env.apply_modifications()
    check_args_contents(cc, test_args[:3] + initial, expected, must_be_gone)


@pytest.mark.regression("9160")
def test_disable_new_dtags(wrapper_environment, wrapper_flags):
    with set_env(SPACK_TEST_COMMAND="dump-args"):
        result = ld(*test_args, output=str).strip().split("\n")
        assert "--disable-new-dtags" in result
        result = cc(*test_args, output=str).strip().split("\n")
        assert "-Wl,--disable-new-dtags" in result


@pytest.mark.regression("9160")
def test_filter_enable_new_dtags(wrapper_environment, wrapper_flags):
    with set_env(SPACK_TEST_COMMAND="dump-args"):
        result = ld(*(test_args + ["--enable-new-dtags"]), output=str)
        result = result.strip().split("\n")
        assert "--enable-new-dtags" not in result

        result = cc(*(test_args + ["-Wl,--enable-new-dtags"]), output=str)
        result = result.strip().split("\n")
        assert "-Wl,--enable-new-dtags" not in result


@pytest.mark.regression("22643")
def test_linker_strips_loopopt(wrapper_environment, wrapper_flags):
    with set_env(SPACK_TEST_COMMAND="dump-args"):
        # ensure that -loopopt=0 is not present in ld mode
        result = ld(*(test_args + ["-loopopt=0"]), output=str)
        result = result.strip().split("\n")
        assert "-loopopt=0" not in result

        # ensure that -loopopt=0 is not present in ccld mode
        result = cc(*(test_args + ["-loopopt=0"]), output=str)
        result = result.strip().split("\n")
        assert "-loopopt=0" not in result

        # ensure that -loopopt=0 *is* present in cc mode
        # The "-c" argument is needed for cc to be detected
        # as compile only (cc) mode.
        result = cc(*(test_args + ["-loopopt=0", "-c", "x.c"]), output=str)
        result = result.strip().split("\n")
        assert "-loopopt=0" in result
