# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
import os
import platform
import sys

import pytest

import llnl.util.filesystem as fs

import spack.concretize
import spack.operating_systems
import spack.platforms
import spack.spec
import spack.target


@pytest.fixture(scope="module")
def current_host_platform():
    """Return the platform of the current host as detected by the
    'platform' stdlib package.
    """
    if os.path.exists("/opt/cray/pe"):
        current_platform = spack.platforms.Cray()
    elif "Linux" in platform.system():
        current_platform = spack.platforms.Linux()
    elif "Darwin" in platform.system():
        current_platform = spack.platforms.Darwin()
    elif "Windows" in platform.system():
        current_platform = spack.platforms.Windows()
    return current_platform


# Valid keywords for os=xxx or target=xxx
VALID_KEYWORDS = ["fe", "be", "frontend", "backend"]

TEST_PLATFORM = spack.platforms.Test()


@pytest.fixture(params=([str(x) for x in TEST_PLATFORM.targets] + VALID_KEYWORDS), scope="module")
def target_str(request):
    """All the possible strings that can be used for targets"""
    return request.param


@pytest.fixture(
    params=([str(x) for x in TEST_PLATFORM.operating_sys] + VALID_KEYWORDS), scope="module"
)
def os_str(request):
    """All the possible strings that can be used for operating systems"""
    return request.param


def test_platform(current_host_platform):
    """Check that current host detection return the correct platform"""
    detected_platform = spack.platforms.real_host()
    assert str(detected_platform) == str(current_host_platform)


@pytest.mark.skipif(sys.platform == "win32", reason="Not supported on Windows (yet)")
def test_user_input_combination(config, target_str, os_str):
    """Test for all the valid user input combinations that both the target and
    the operating system match.
    """
    spec_str = "libelf os={} target={}".format(os_str, target_str)
    spec = spack.spec.Spec(spec_str)
    assert spec.architecture.os == str(TEST_PLATFORM.operating_system(os_str))
    assert spec.architecture.target == TEST_PLATFORM.target(target_str)


def test_default_os_and_target(default_mock_concretization):
    """Test that is we don't specify `os=` or `target=` we get the default values
    after concretization.
    """
    spec = default_mock_concretization("libelf")
    assert spec.architecture.os == str(TEST_PLATFORM.operating_system("default_os"))
    assert spec.architecture.target == TEST_PLATFORM.target("default_target")


def test_operating_system_conversion_to_dict():
    operating_system = spack.operating_systems.OperatingSystem("os", "1.0")
    assert operating_system.to_dict() == {"name": "os", "version": "1.0"}


@pytest.mark.parametrize(
    "cpu_flag,target_name",
    [
        # Test that specific flags can be used in queries
        ("ssse3", "haswell"),
        ("popcnt", "nehalem"),
        ("avx512f", "skylake_avx512"),
        ("avx512ifma", "icelake"),
        # Test that proxy flags can be used in queries too
        ("sse3", "nehalem"),
        ("avx512", "skylake_avx512"),
        ("avx512", "icelake"),
    ],
)
def test_target_container_semantic(cpu_flag, target_name):
    target = spack.target.Target(target_name)
    assert cpu_flag in target


@pytest.mark.parametrize(
    "item,architecture_str",
    [
        # We can search the architecture string representation
        ("linux", "linux-ubuntu18.04-haswell"),
        ("ubuntu", "linux-ubuntu18.04-haswell"),
        ("haswell", "linux-ubuntu18.04-haswell"),
        # We can also search flags of the target,
        ("avx512", "linux-ubuntu18.04-icelake"),
    ],
)
def test_arch_spec_container_semantic(item, architecture_str):
    architecture = spack.spec.ArchSpec(architecture_str)
    assert item in architecture


@pytest.mark.parametrize(
    "compiler_spec,target_name,expected_flags",
    [
        # Check compilers with version numbers from a single toolchain
        ("gcc@4.7.2", "ivybridge", "-march=core-avx-i -mtune=core-avx-i"),
        # Check mixed toolchains
        ("clang@8.0.0", "broadwell", ""),
        ("clang@3.5", "x86_64", "-march=x86-64 -mtune=generic"),
        # Check Apple's Clang compilers
        ("apple-clang@9.1.0", "x86_64", "-march=x86-64"),
    ],
)
@pytest.mark.filterwarnings("ignore:microarchitecture specific")
def test_optimization_flags(compiler_spec, target_name, expected_flags, config):
    target = spack.target.Target(target_name)
    compiler = spack.compilers.compilers_for_spec(compiler_spec).pop()
    opt_flags = target.optimization_flags(compiler)
    assert opt_flags == expected_flags


@pytest.mark.parametrize(
    "compiler,real_version,target_str,expected_flags",
    [
        (spack.spec.CompilerSpec("gcc@9.2.0"), None, "haswell", "-march=haswell -mtune=haswell"),
        # Check that custom string versions are accepted
        (
            spack.spec.CompilerSpec("gcc@10foo"),
            "9.2.0",
            "icelake",
            "-march=icelake-client -mtune=icelake-client",
        ),
        # Check that we run version detection (4.4.0 doesn't support icelake)
        (
            spack.spec.CompilerSpec("gcc@4.4.0-special"),
            "9.2.0",
            "icelake",
            "-march=icelake-client -mtune=icelake-client",
        ),
        # Check that the special case for Apple's clang is treated correctly
        # i.e. it won't try to detect the version again
        (spack.spec.CompilerSpec("apple-clang@9.1.0"), None, "x86_64", "-march=x86-64"),
    ],
)
def test_optimization_flags_with_custom_versions(
    compiler, real_version, target_str, expected_flags, monkeypatch, config
):
    target = spack.target.Target(target_str)
    if real_version:
        monkeypatch.setattr(spack.compiler.Compiler, "get_real_version", lambda x: real_version)
    opt_flags = target.optimization_flags(compiler)
    assert opt_flags == expected_flags


@pytest.mark.regression("15306")
@pytest.mark.parametrize(
    "architecture_tuple,constraint_tuple",
    [
        (("linux", "ubuntu18.04", None), ("linux", None, "x86_64")),
        (("linux", "ubuntu18.04", None), ("linux", None, "x86_64:")),
    ],
)
def test_satisfy_strict_constraint_when_not_concrete(architecture_tuple, constraint_tuple):
    architecture = spack.spec.ArchSpec(architecture_tuple)
    constraint = spack.spec.ArchSpec(constraint_tuple)
    assert not architecture.satisfies(constraint)


@pytest.mark.parametrize(
    "root_target_range,dep_target_range,result",
    [
        ("x86_64:nocona", "x86_64:core2", "nocona"),  # pref not in intersection
        ("x86_64:core2", "x86_64:nocona", "nocona"),
        ("x86_64:haswell", "x86_64:mic_knl", "core2"),  # pref in intersection
        ("ivybridge", "nocona:skylake", "ivybridge"),  # one side concrete
        ("haswell:icelake", "broadwell", "broadwell"),
        # multiple ranges in lists with multiple overlaps
        ("x86_64:nocona,haswell:broadwell", "nocona:haswell,skylake:", "nocona"),
        # lists with concrete targets, lists compared to ranges
        ("x86_64,haswell", "core2:broadwell", "haswell"),
    ],
)
@pytest.mark.usefixtures("mock_packages", "config")
def test_concretize_target_ranges(root_target_range, dep_target_range, result, monkeypatch):
    # Monkeypatch so that all concretization is done as if the machine is core2
    monkeypatch.setattr(spack.platforms.test.Test, "default", "core2")

    # use foobar=bar to make the problem simpler for the old concretizer
    # the new concretizer should not need that help
    if spack.config.get("config:concretizer") == "original":
        pytest.skip("Fixing the parser broke this test for the original concretizer.")

    spec_str = "a %%gcc@10 foobar=bar target=%s ^b target=%s" % (
        root_target_range,
        dep_target_range,
    )
    spec = spack.spec.Spec(spec_str)
    with spack.concretize.disable_compiler_existence_check():
        spec.concretize()

    assert str(spec).count("arch=test-debian6-%s" % result) == 2


@pytest.mark.parametrize(
    "versions,default,expected",
    [
        (["21.11", "21.9"], "21.11", False),
        (["21.11", "21.9"], "21.9", True),
        (["21.11", "21.9"], None, False),
    ],
)
def test_cray_platform_detection(versions, default, expected, tmpdir, monkeypatch, working_env):
    ex_path = str(tmpdir.join("fake_craype_dir"))
    fs.mkdirp(ex_path)

    with fs.working_dir(ex_path):
        for version in versions:
            fs.touch(version)
        if default:
            os.symlink(default, "default")

    monkeypatch.setattr(spack.platforms.cray, "_ex_craype_dir", ex_path)
    os.environ["MODULEPATH"] = "/opt/cray/pe"

    assert spack.platforms.cray.Cray.detect() == expected
