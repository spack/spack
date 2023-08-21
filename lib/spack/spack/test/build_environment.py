# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
import inspect
import os
import platform
import posixpath

import pytest

from llnl.util.filesystem import HeaderList, LibraryList

import spack.build_environment
import spack.config
import spack.package_base
import spack.spec
import spack.util.spack_yaml as syaml
from spack.build_environment import _static_to_shared_library, determine_number_of_jobs, dso_suffix
from spack.paths import build_env_path
from spack.util.environment import EnvironmentModifications
from spack.util.executable import Executable
from spack.util.path import Path, convert_to_platform_path


def os_pathsep_join(path, *pths):
    out_pth = path
    for pth in pths:
        out_pth = os.pathsep.join([out_pth, pth])
    return out_pth


def prep_and_join(path, *pths):
    return os.path.sep + os.path.join(path, *pths)


@pytest.fixture
def build_environment(working_env):
    cc = Executable(os.path.join(build_env_path, "cc"))
    cxx = Executable(os.path.join(build_env_path, "c++"))
    fc = Executable(os.path.join(build_env_path, "fc"))

    realcc = "/bin/mycc"
    prefix = "/spack-test-prefix"

    os.environ["SPACK_CC"] = realcc
    os.environ["SPACK_CXX"] = realcc
    os.environ["SPACK_FC"] = realcc

    os.environ["SPACK_PREFIX"] = prefix
    os.environ["SPACK_ENV_PATH"] = "test"
    os.environ["SPACK_DEBUG_LOG_DIR"] = "."
    os.environ["SPACK_DEBUG_LOG_ID"] = "foo-hashabc"
    os.environ["SPACK_COMPILER_SPEC"] = "gcc@4.4.7"
    os.environ["SPACK_SHORT_SPEC"] = "foo@1.2 arch=linux-rhel6-x86_64 /hashabc"

    os.environ["SPACK_CC_RPATH_ARG"] = "-Wl,-rpath,"
    os.environ["SPACK_CXX_RPATH_ARG"] = "-Wl,-rpath,"
    os.environ["SPACK_F77_RPATH_ARG"] = "-Wl,-rpath,"
    os.environ["SPACK_FC_RPATH_ARG"] = "-Wl,-rpath,"
    os.environ["SPACK_LINKER_ARG"] = "-Wl,"
    os.environ["SPACK_DTAGS_TO_ADD"] = "--disable-new-dtags"
    os.environ["SPACK_DTAGS_TO_STRIP"] = "--enable-new-dtags"
    os.environ["SPACK_SYSTEM_DIRS"] = "/usr/include /usr/lib"
    os.environ["SPACK_TARGET_ARGS"] = ""

    if "SPACK_DEPENDENCIES" in os.environ:
        del os.environ["SPACK_DEPENDENCIES"]

    yield {"cc": cc, "cxx": cxx, "fc": fc}

    for name in (
        "SPACK_CC",
        "SPACK_CXX",
        "SPACK_FC",
        "SPACK_PREFIX",
        "SPACK_ENV_PATH",
        "SPACK_DEBUG_LOG_DIR",
        "SPACK_COMPILER_SPEC",
        "SPACK_SHORT_SPEC",
        "SPACK_CC_RPATH_ARG",
        "SPACK_CXX_RPATH_ARG",
        "SPACK_F77_RPATH_ARG",
        "SPACK_FC_RPATH_ARG",
        "SPACK_TARGET_ARGS",
    ):
        del os.environ[name]


@pytest.fixture
def ensure_env_variables(config, mock_packages, monkeypatch, working_env):
    """Returns a function that takes a dictionary and updates os.environ
    for the test lifetime accordingly. Plugs-in mock config and repo.
    """

    def _ensure(env_mods):
        for name, value in env_mods.items():
            monkeypatch.setenv(name, value)

    return _ensure


@pytest.fixture
def mock_module_cmd(monkeypatch):
    class Logger:
        def __init__(self, fn=None):
            self.fn = fn
            self.calls = []

        def __call__(self, *args, **kwargs):
            self.calls.append((args, kwargs))
            if self.fn:
                return self.fn(*args, **kwargs)

    mock_module_cmd = Logger()
    monkeypatch.setattr(spack.build_environment, "module", mock_module_cmd)
    monkeypatch.setattr(spack.build_environment, "_on_cray", lambda: (True, None))
    return mock_module_cmd


@pytest.mark.not_on_windows("Static to Shared not supported on Win (yet)")
def test_static_to_shared_library(build_environment):
    os.environ["SPACK_TEST_COMMAND"] = "dump-args"

    expected = {
        "linux": (
            "/bin/mycc -shared"
            " -Wl,--disable-new-dtags"
            " -Wl,-soname -Wl,{2} -Wl,--whole-archive {0}"
            " -Wl,--no-whole-archive -o {1}"
        ),
        "darwin": (
            "/bin/mycc -dynamiclib"
            " -Wl,--disable-new-dtags"
            " -install_name {1} -Wl,-force_load -Wl,{0} -o {1}"
        ),
    }

    static_lib = "/spack/libfoo.a"

    for arch in ("linux", "darwin"):
        for shared_lib in (None, "/spack/libbar.so"):
            output = _static_to_shared_library(
                arch, build_environment["cc"], static_lib, shared_lib, compiler_output=str
            ).strip()

            if not shared_lib:
                shared_lib = "{0}.{1}".format(os.path.splitext(static_lib)[0], dso_suffix)

            assert set(output.split()) == set(
                expected[arch].format(static_lib, shared_lib, os.path.basename(shared_lib)).split()
            )


@pytest.mark.regression("8345")
@pytest.mark.usefixtures("config", "mock_packages")
def test_cc_not_changed_by_modules(monkeypatch, working_env):
    s = spack.spec.Spec("cmake")
    s.concretize()
    pkg = s.package

    def _set_wrong_cc(x):
        os.environ["CC"] = "NOT_THIS_PLEASE"
        os.environ["ANOTHER_VAR"] = "THIS_IS_SET"

    monkeypatch.setattr(spack.build_environment, "load_module", _set_wrong_cc)
    monkeypatch.setattr(pkg.compiler, "modules", ["some_module"])

    spack.build_environment.setup_package(pkg, False)

    assert os.environ["CC"] != "NOT_THIS_PLEASE"
    assert os.environ["ANOTHER_VAR"] == "THIS_IS_SET"


def test_setup_dependent_package_inherited_modules(
    config, working_env, mock_packages, install_mockery, mock_fetch
):
    # This will raise on regression
    s = spack.spec.Spec("cmake-client-inheritor").concretized()
    s.package.do_install()


@pytest.mark.parametrize(
    "initial,modifications,expected",
    [
        # Set and unset variables
        (
            {"SOME_VAR_STR": "", "SOME_VAR_NUM": "0"},
            {"set": {"SOME_VAR_STR": "SOME_STR", "SOME_VAR_NUM": 1}},
            {"SOME_VAR_STR": "SOME_STR", "SOME_VAR_NUM": "1"},
        ),
        ({"SOME_VAR_STR": ""}, {"unset": ["SOME_VAR_STR"]}, {"SOME_VAR_STR": None}),
        (
            {},  # Set a variable that was not defined already
            {"set": {"SOME_VAR_STR": "SOME_STR"}},
            {"SOME_VAR_STR": "SOME_STR"},
        ),
        # Append and prepend to the same variable
        (
            {"EMPTY_PATH_LIST": prep_and_join("path", "middle")},
            {
                "prepend_path": {"EMPTY_PATH_LIST": prep_and_join("path", "first")},
                "append_path": {"EMPTY_PATH_LIST": prep_and_join("path", "last")},
            },
            {
                "EMPTY_PATH_LIST": os_pathsep_join(
                    prep_and_join("path", "first"),
                    prep_and_join("path", "middle"),
                    prep_and_join("path", "last"),
                )
            },
        ),
        # Append and prepend from empty variables
        (
            {"EMPTY_PATH_LIST": "", "SOME_VAR_STR": ""},
            {
                "prepend_path": {"EMPTY_PATH_LIST": prep_and_join("path", "first")},
                "append_path": {"SOME_VAR_STR": prep_and_join("path", "last")},
            },
            {
                "EMPTY_PATH_LIST": prep_and_join("path", "first"),
                "SOME_VAR_STR": prep_and_join("path", "last"),
            },
        ),
        (
            {},  # Same as before but on variables that were not defined
            {
                "prepend_path": {"EMPTY_PATH_LIST": prep_and_join("path", "first")},
                "append_path": {"SOME_VAR_STR": prep_and_join("path", "last")},
            },
            {
                "EMPTY_PATH_LIST": prep_and_join("path", "first"),
                "SOME_VAR_STR": prep_and_join("path", "last"),
            },
        ),
        # Remove a path from a list
        (
            {
                "EMPTY_PATH_LIST": os_pathsep_join(
                    prep_and_join("path", "first"),
                    prep_and_join("path", "middle"),
                    prep_and_join("path", "last"),
                )
            },
            {"remove_path": {"EMPTY_PATH_LIST": prep_and_join("path", "middle")}},
            {
                "EMPTY_PATH_LIST": os_pathsep_join(
                    prep_and_join("path", "first"), prep_and_join("path", "last")
                )
            },
        ),
        (
            {"EMPTY_PATH_LIST": prep_and_join("only", "path")},
            {"remove_path": {"EMPTY_PATH_LIST": prep_and_join("only", "path")}},
            {"EMPTY_PATH_LIST": ""},
        ),
    ],
)
def test_compiler_config_modifications(
    initial, modifications, expected, ensure_env_variables, monkeypatch
):
    # Set the environment as per prerequisites
    ensure_env_variables(initial)

    def platform_pathsep(pathlist):
        if Path.platform_path == Path.windows:
            pathlist = pathlist.replace(":", ";")

        return convert_to_platform_path(pathlist)

    # Monkeypatch a pkg.compiler.environment with the required modifications
    pkg = spack.spec.Spec("cmake").concretized().package
    monkeypatch.setattr(pkg.compiler, "environment", modifications)
    # Trigger the modifications
    spack.build_environment.setup_package(pkg, False)

    # Check they were applied
    for name, value in expected.items():
        if value is not None:
            value = platform_pathsep(value)
            assert os.environ[name] == value
            continue
        assert name not in os.environ


@pytest.mark.regression("9107")
def test_spack_paths_before_module_paths(config, mock_packages, monkeypatch, working_env):
    s = spack.spec.Spec("cmake")
    s.concretize()
    pkg = s.package

    module_path = os.path.join("path", "to", "module")

    def _set_wrong_cc(x):
        os.environ["PATH"] = module_path + os.pathsep + os.environ["PATH"]

    monkeypatch.setattr(spack.build_environment, "load_module", _set_wrong_cc)
    monkeypatch.setattr(pkg.compiler, "modules", ["some_module"])

    spack.build_environment.setup_package(pkg, False)

    spack_path = os.path.join(spack.paths.prefix, os.path.join("lib", "spack", "env"))

    paths = os.environ["PATH"].split(os.pathsep)

    assert paths.index(spack_path) < paths.index(module_path)


def test_package_inheritance_module_setup(config, mock_packages, working_env):
    s = spack.spec.Spec("multimodule-inheritance")
    s.concretize()
    pkg = s.package

    spack.build_environment.setup_package(pkg, False)

    os.environ["TEST_MODULE_VAR"] = "failed"

    assert pkg.use_module_variable() == "test_module_variable"
    assert os.environ["TEST_MODULE_VAR"] == "test_module_variable"


def test_wrapper_variables(
    config, mock_packages, working_env, monkeypatch, installation_dir_with_headers
):
    """Check that build_environment supplies the needed library/include
    directories via the SPACK_LINK_DIRS and SPACK_INCLUDE_DIRS environment
    variables.
    """

    # https://github.com/spack/spack/issues/13969
    cuda_headers = HeaderList(
        [
            "prefix/include/cuda_runtime.h",
            "prefix/include/cuda/atomic",
            "prefix/include/cuda/std/detail/libcxx/include/ctype.h",
        ]
    )
    cuda_include_dirs = cuda_headers.directories
    assert posixpath.join("prefix", "include") in cuda_include_dirs
    assert (
        posixpath.join("prefix", "include", "cuda", "std", "detail", "libcxx", "include")
        not in cuda_include_dirs
    )

    root = spack.spec.Spec("dt-diamond")
    root.concretize()

    for s in root.traverse():
        s.prefix = "/{0}-prefix/".format(s.name)

    dep_pkg = root["dt-diamond-left"].package
    dep_lib_paths = ["/test/path/to/ex1.so", "/test/path/to/subdir/ex2.so"]
    dep_lib_dirs = ["/test/path/to", "/test/path/to/subdir"]
    dep_libs = LibraryList(dep_lib_paths)

    dep2_pkg = root["dt-diamond-right"].package
    dep2_pkg.spec.prefix = str(installation_dir_with_headers)

    setattr(dep_pkg, "libs", dep_libs)
    try:
        pkg = root.package
        env_mods = EnvironmentModifications()
        spack.build_environment.set_wrapper_variables(pkg, env_mods)

        env_mods.apply_modifications()

        def normpaths(paths):
            return list(os.path.normpath(p) for p in paths)

        link_dir_var = os.environ["SPACK_LINK_DIRS"]
        assert normpaths(link_dir_var.split(":")) == normpaths(dep_lib_dirs)

        root_libdirs = ["/dt-diamond-prefix/lib", "/dt-diamond-prefix/lib64"]
        rpath_dir_var = os.environ["SPACK_RPATH_DIRS"]
        # The 'lib' and 'lib64' subdirectories of the root package prefix
        # should always be rpathed and should be the first rpaths
        assert normpaths(rpath_dir_var.split(":")) == normpaths(root_libdirs + dep_lib_dirs)

        header_dir_var = os.environ["SPACK_INCLUDE_DIRS"]

        # The default implementation looks for header files only
        # in <prefix>/include and subdirectories
        prefix = str(installation_dir_with_headers)
        include_dirs = normpaths(header_dir_var.split(os.pathsep))

        assert os.path.join(prefix, "include") in include_dirs
        assert os.path.join(prefix, "include", "boost") not in include_dirs
        assert os.path.join(prefix, "path", "to") not in include_dirs
        assert os.path.join(prefix, "path", "to", "subdir") not in include_dirs

    finally:
        delattr(dep_pkg, "libs")


def test_external_prefixes_last(mutable_config, mock_packages, working_env, monkeypatch):
    # Sanity check: under normal circumstances paths associated with
    # dt-diamond-left would appear first. We'll mark it as external in
    # the test to check if the associated paths are placed last.
    assert "dt-diamond-left" < "dt-diamond-right"

    cfg_data = syaml.load_config(
        """\
dt-diamond-left:
  externals:
  - spec: dt-diamond-left@1.0
    prefix: /fake/path1
  buildable: false
"""
    )
    spack.config.set("packages", cfg_data)
    top = spack.spec.Spec("dt-diamond").concretized()

    def _trust_me_its_a_dir(path):
        return True

    monkeypatch.setattr(os.path, "isdir", _trust_me_its_a_dir)

    env_mods = EnvironmentModifications()
    spack.build_environment.set_wrapper_variables(top.package, env_mods)

    env_mods.apply_modifications()
    link_dir_var = os.environ["SPACK_LINK_DIRS"]
    link_dirs = link_dir_var.split(":")
    external_lib_paths = set(
        [os.path.normpath("/fake/path1/lib"), os.path.normpath("/fake/path1/lib64")]
    )
    # The external lib paths should be the last two entries of the list and
    # should not appear anywhere before the last two entries
    assert set(os.path.normpath(x) for x in link_dirs[-2:]) == external_lib_paths
    assert not (set(os.path.normpath(x) for x in link_dirs[:-2]) & external_lib_paths)


def test_parallel_false_is_not_propagating(default_mock_concretization):
    """Test that parallel=False is not propagating to dependencies"""
    # a foobar=bar (parallel = False)
    # |
    # b (parallel =True)
    s = default_mock_concretization("a foobar=bar")

    spack.build_environment.set_module_variables_for_package(s.package)
    assert s["a"].package.module.make_jobs == 1

    spack.build_environment.set_module_variables_for_package(s["b"].package)
    assert s["b"].package.module.make_jobs == spack.build_environment.determine_number_of_jobs(
        s["b"].package.parallel
    )


@pytest.mark.parametrize(
    "config_setting,expected_flag",
    [
        ("runpath", "" if platform.system() == "Darwin" else "--enable-new-dtags"),
        ("rpath", "" if platform.system() == "Darwin" else "--disable-new-dtags"),
    ],
)
def test_setting_dtags_based_on_config(config_setting, expected_flag, config, mock_packages):
    # Pick a random package to be able to set compiler's variables
    s = spack.spec.Spec("cmake")
    s.concretize()
    pkg = s.package

    env = EnvironmentModifications()
    with spack.config.override("config:shared_linking", {"type": config_setting, "bind": False}):
        spack.build_environment.set_compiler_environment_variables(pkg, env)
        modifications = env.group_by_name()
        assert "SPACK_DTAGS_TO_STRIP" in modifications
        assert "SPACK_DTAGS_TO_ADD" in modifications
        assert len(modifications["SPACK_DTAGS_TO_ADD"]) == 1
        assert len(modifications["SPACK_DTAGS_TO_STRIP"]) == 1

        dtags_to_add = modifications["SPACK_DTAGS_TO_ADD"][0]
        assert dtags_to_add.value == expected_flag


def test_build_jobs_sequential_is_sequential():
    assert (
        determine_number_of_jobs(parallel=False, command_line=8, config_default=8, max_cpus=8) == 1
    )


def test_build_jobs_command_line_overrides():
    assert (
        determine_number_of_jobs(parallel=True, command_line=10, config_default=1, max_cpus=1)
        == 10
    )
    assert (
        determine_number_of_jobs(parallel=True, command_line=10, config_default=100, max_cpus=100)
        == 10
    )


def test_build_jobs_defaults():
    assert (
        determine_number_of_jobs(parallel=True, command_line=None, config_default=1, max_cpus=10)
        == 1
    )
    assert (
        determine_number_of_jobs(parallel=True, command_line=None, config_default=100, max_cpus=10)
        == 10
    )


def test_dirty_disable_module_unload(config, mock_packages, working_env, mock_module_cmd):
    """Test that on CRAY platform 'module unload' is not called if the 'dirty'
    option is on.
    """
    s = spack.spec.Spec("a").concretized()

    # If called with "dirty" we don't unload modules, so no calls to the
    # `module` function on Cray
    spack.build_environment.setup_package(s.package, dirty=True)
    assert not mock_module_cmd.calls

    # If called without "dirty" we unload modules on Cray
    spack.build_environment.setup_package(s.package, dirty=False)
    assert mock_module_cmd.calls
    assert any(("unload", "cray-libsci") == item[0] for item in mock_module_cmd.calls)
    assert any(("unload", "cray-mpich") == item[0] for item in mock_module_cmd.calls)


class TestModuleMonkeyPatcher:
    def test_getting_attributes(self, default_mock_concretization):
        s = default_mock_concretization("libelf")
        module_wrapper = spack.build_environment.ModuleChangePropagator(s.package)
        assert module_wrapper.Libelf == s.package.module.Libelf

    def test_setting_attributes(self, default_mock_concretization):
        s = default_mock_concretization("libelf")
        module = s.package.module
        module_wrapper = spack.build_environment.ModuleChangePropagator(s.package)

        # Setting an attribute has an immediate effect
        module_wrapper.SOME_ATTRIBUTE = 1
        assert module.SOME_ATTRIBUTE == 1

        # We can also propagate the settings to classes in the MRO
        module_wrapper.propagate_changes_to_mro()
        for cls in inspect.getmro(type(s.package)):
            current_module = cls.module
            if current_module == spack.package_base:
                break
            assert current_module.SOME_ATTRIBUTE == 1
