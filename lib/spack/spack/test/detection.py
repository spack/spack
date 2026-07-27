# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
import collections
import json
import pathlib
import sys

import pytest

import spack.detection
import spack.detection.common
import spack.detection.path
import spack.operating_systems.windows_os as win_os
import spack.repo
import spack.spec
from spack.config import Configuration
from spack.test.utilities import UnusableGlobal


def test_detection_update_config(mutable_config: Configuration):
    # mock detected package
    detected_packages = collections.defaultdict(list)
    detected_packages["cmake"] = [spack.spec.Spec("cmake@3.27.5", external_path="/usr/bin")]

    # update config for new package
    spack.detection.common.update_configuration(detected_packages, config=mutable_config)
    # Check entries in 'packages.yaml'
    packages_yaml = mutable_config.get("packages")
    assert "cmake" in packages_yaml
    assert "externals" in packages_yaml["cmake"]
    externals = packages_yaml["cmake"]["externals"]
    assert len(externals) == 1
    external_gcc = externals[0]
    assert external_gcc["spec"] == "cmake@3.27.5"
    assert external_gcc["prefix"] == "/usr/bin"


def test_dedupe_paths(tmp_path: pathlib.Path):
    """Test that ``dedupe_paths`` deals with symlinked directories, retaining the target"""
    x = tmp_path / "x"
    y = tmp_path / "y"
    z = tmp_path / "z"

    x.mkdir()
    y.mkdir()
    z.symlink_to("x", target_is_directory=True)

    # dedupe repeated dirs, should preserve order
    assert spack.detection.path.dedupe_paths([str(x), str(y), str(x)]) == [str(x), str(y)]
    assert spack.detection.path.dedupe_paths([str(y), str(x), str(y)]) == [str(y), str(x)]

    # dedupe repeated symlinks
    assert spack.detection.path.dedupe_paths([str(z), str(y), str(z)]) == [str(z), str(y)]
    assert spack.detection.path.dedupe_paths([str(y), str(z), str(y)]) == [str(y), str(z)]

    # when both symlink and target are present, only target is retained, and it comes at the
    # priority of the first occurrence.
    assert spack.detection.path.dedupe_paths([str(x), str(y), str(z)]) == [str(x), str(y)]
    assert spack.detection.path.dedupe_paths([str(z), str(y), str(x)]) == [str(x), str(y)]
    assert spack.detection.path.dedupe_paths([str(y), str(z), str(x)]) == [str(y), str(x)]


def test_detect_specs_deduplicates_across_prefixes(tmp_path, monkeypatch, mock_packages):
    """Tests that the same spec detected at two different prefixes should yield only one result.

    Returning both causes duplicate externals in packages.yaml and non-deterministic hashes
    during concretization.
    """
    # Create two independent bin/ directories, each containing the same executable name.
    prefix_a = tmp_path / "prefix_a"
    prefix_b = tmp_path / "prefix_b"
    (prefix_a / "bin").mkdir(parents=True)
    (prefix_b / "bin").mkdir(parents=True)
    exe_a = prefix_a / "bin" / "cmake"
    exe_b = prefix_b / "bin" / "cmake"
    exe_a.touch()
    exe_b.touch()

    cmake_cls = mock_packages.get_pkg_class("cmake")

    # Patch determine_spec_details to always return the same spec, regardless of prefix.
    @classmethod
    def _same_spec(cls, prefix, exes_in_prefix):
        return spack.spec.Spec("cmake@3.17.1")

    monkeypatch.setattr(cmake_cls, "determine_spec_details", _same_spec)

    finder = spack.detection.path.ExecutablesFinder()
    detected = finder.detect_specs(
        pkg=cmake_cls, paths=[str(exe_a), str(exe_b)], repo_path=mock_packages
    )

    # Both prefixes produce cmake@3.17.1; only the first should be kept.
    assert len(detected) == 1


def test_prefix_cuts_at_last_bin_or_lib(tmp_path: pathlib.Path):
    """Prefixes should be cut at the LAST occurrence
    of bin/lib/lib64, not the first, so nested paths like .../bin/gcc/bin don't
    produce a garbage prefix."""

    # nested bin: only the last "bin" should be cut
    nested_bin = tmp_path / "bin" / "gcc" / "bin"
    nested_bin.mkdir(parents=True)
    expected_bin = str(tmp_path / "bin" / "gcc")
    assert spack.detection.common.executable_prefix(str(nested_bin)) == expected_bin

    # simple, single "bin"
    simple_bin = tmp_path / "simple" / "bin"
    simple_bin.mkdir(parents=True)
    assert spack.detection.common.executable_prefix(str(simple_bin)) == str(tmp_path / "simple")

    # no "bin" component at all
    no_bin = tmp_path / "opt" / "gcc"
    no_bin.mkdir(parents=True)
    assert spack.detection.common.executable_prefix(str(no_bin)) == str(no_bin)

    # nested lib: only the last "lib" should be cut
    nested_lib = tmp_path / "lib" / "foo" / "lib"
    nested_lib.mkdir(parents=True)
    expected_lib = str(tmp_path / "lib" / "foo")
    assert spack.detection.common.library_prefix(str(nested_lib)) == expected_lib

    # nested lib64: only the last "lib64" should be cut
    nested_lib64 = tmp_path / "lib64" / "foo" / "lib64"
    nested_lib64.mkdir(parents=True)
    expected_lib64 = str(tmp_path / "lib64" / "foo")
    assert spack.detection.common.library_prefix(str(nested_lib64)) == expected_lib64

    # the innermost recognized component wins, regardless of its name
    mixed_lib = tmp_path / "lib64" / "foo" / "lib"
    mixed_lib.mkdir(parents=True)
    assert spack.detection.common.library_prefix(str(mixed_lib)) == str(tmp_path / "lib64" / "foo")


def test_prefix_before_last_supports_windows_paths():
    path = pathlib.PureWindowsPath(r"C:\Apps\Lib64\foo\LIB")
    assert (
        spack.detection.common.prefix_before_last(path, ("lib", "lib64")) == r"C:\Apps\Lib64\foo"
    )


@pytest.mark.skipif(sys.platform != "win32", reason="Skip Windows paths on not Windows")
def test_library_prefix_cuts_at_bin_on_windows(tmp_path: pathlib.Path):
    """On Windows, library prefixes fall back to cutting at the last bin directory."""
    nested_win_bin = tmp_path / "winbin" / "foo" / "bin"
    nested_win_bin.mkdir(parents=True)
    expected_win_bin = str(tmp_path / "winbin" / "foo")
    assert spack.detection.common.library_prefix(str(nested_win_bin)) == expected_win_bin


def test_detect_specs_validates_variants_with_injected_repo(tmp_path, monkeypatch, mock_packages):
    """Tests that the variants of the specs returned by determine_spec_details are validated
    against the repository passed to detect_specs, and that invalid specs are discarded.
    """
    prefixes = {"valid": tmp_path / "valid", "invalid": tmp_path / "invalid"}
    for prefix in prefixes.values():
        (prefix / "bin").mkdir(parents=True)
        (prefix / "bin" / "gcc").touch()

    gcc_cls = mock_packages.get_pkg_class("gcc")

    @classmethod
    def _determine_spec_details(cls, prefix, exes_in_prefix):
        languages = "c,c++" if prefix == str(prefixes["valid"] / "bin") else "klingon"
        return spack.spec.Spec.from_detection(
            f"gcc@9.4.0 languages={languages}", external_path=str(prefix)
        )

    monkeypatch.setattr(gcc_cls, "determine_spec_details", _determine_spec_details)

    with monkeypatch.context() as m:
        m.setattr(spack.repo, "PATH", UnusableGlobal("spack.repo.PATH"))
        detected = spack.detection.path.ExecutablesFinder().detect_specs(
            pkg=gcc_cls,
            paths=[str(p / "bin" / "gcc") for p in prefixes.values()],
            repo_path=mock_packages,
        )

    assert len(detected) == 1
    assert detected[0].external_path == str(prefixes["valid"] / "bin")
    assert detected[0].satisfies("languages=c,c++")


_SDK_VER = "10.0.22621.0"


@pytest.fixture()
def vs_root(tmp_path):
    """Minimal VS installation tree with CMake, Ninja, and LLVM components."""
    root = tmp_path / "VS2022"
    cmake_bin = (
        root / "Common7" / "IDE" / "CommonExtensions" / "Microsoft" / "CMake" / "CMake" / "bin"
    )
    cmake_bin.mkdir(parents=True)
    ninja_dir = root / "Common7" / "IDE" / "CommonExtensions" / "Microsoft" / "CMake" / "Ninja"
    ninja_dir.mkdir(parents=True)
    (root / "VC" / "Tools" / "Llvm" / "x64" / "bin").mkdir(parents=True)
    (root / "VC" / "Tools" / "Llvm" / "ARM64" / "bin").mkdir(parents=True)
    return root


@pytest.fixture()
def kit_root(tmp_path):
    """Minimal Windows Kits 10 tree with SDK bin/lib and WDK km dirs."""
    pf86 = tmp_path / "ProgramFiles86"
    kit = pf86 / "Windows Kits" / "10"
    for arch in ("x64", "x86"):
        (kit / "bin" / _SDK_VER / arch).mkdir(parents=True)
    for api in ("um", "ucrt"):
        (kit / "Lib" / _SDK_VER / api / "x64").mkdir(parents=True)
    (kit / "Lib" / _SDK_VER / "km" / "x64").mkdir(parents=True)
    return pf86


@pytest.fixture()
def vs_state_json(tmp_path, vs_root, kit_root):
    """VS instance state.json declaring SDK packages for vs_root."""
    programdata = tmp_path / "ProgramData"
    instance_dir = (
        programdata / "Microsoft" / "VisualStudio" / "Packages" / "_Instances" / "ABCDEF"
    )
    instance_dir.mkdir(parents=True)
    state = {
        "installationPath": str(vs_root),
        "packages": [
            {"id": "Microsoft.Windows.SDK.CPP", "version": _SDK_VER},
            {"id": "Microsoft.Windows.UniversalCRT.Tools.x64", "version": _SDK_VER},
        ],
    }
    (instance_dir / "state.json").write_text(json.dumps(state), encoding="utf-8")
    return programdata


def _patch_vs_root(monkeypatch, root):
    monkeypatch.setattr(win_os.VisualStudioLayout, "find_vs_install_paths", lambda: [str(root)])


def test_vs_layout_cmake(vs_root, monkeypatch):
    _patch_vs_root(monkeypatch, vs_root)
    paths = win_os.VisualStudioLayout.find_cmake_paths()
    expected = str(
        vs_root / "Common7" / "IDE" / "CommonExtensions" / "Microsoft" / "CMake" / "CMake" / "bin"
    )
    assert paths == [expected]


def test_vs_layout_ninja(vs_root, monkeypatch):
    _patch_vs_root(monkeypatch, vs_root)
    paths = win_os.VisualStudioLayout.find_ninja_paths()
    expected = str(
        vs_root / "Common7" / "IDE" / "CommonExtensions" / "Microsoft" / "CMake" / "Ninja"
    )
    assert paths == [expected]


def test_vs_layout_llvm_full(vs_root, monkeypatch):
    """Both per-arch LLVM bin dirs are returned; the old flat fallback is not."""
    _patch_vs_root(monkeypatch, vs_root)
    paths = win_os.VisualStudioLayout.find_llvm_paths()
    assert str(vs_root / "VC" / "Tools" / "Llvm" / "x64" / "bin") in paths
    assert str(vs_root / "VC" / "Tools" / "Llvm" / "ARM64" / "bin") in paths
    assert str(vs_root / "VC" / "Tools" / "Llvm" / "bin") not in paths


def test_vs_layout_llvm_fallback(tmp_path, monkeypatch):
    """Older VS layout without per-arch subdirectories uses the flat bin/ fallback."""
    root = tmp_path / "VS2017"
    (root / "VC" / "Tools" / "Llvm" / "bin").mkdir(parents=True)
    _patch_vs_root(monkeypatch, root)
    paths = win_os.VisualStudioLayout.find_llvm_paths()
    assert paths == [str(root / "VC" / "Tools" / "Llvm" / "bin")]


def test_vs_layout_llvm_absent(tmp_path, monkeypatch):
    """No LLVM component installed yields an empty list."""
    root = tmp_path / "VS_no_llvm"
    root.mkdir()
    _patch_vs_root(monkeypatch, root)
    assert win_os.VisualStudioLayout.find_llvm_paths() == []


def test_vs_layout_sdk_bin(vs_root, kit_root, vs_state_json, monkeypatch):
    monkeypatch.setenv("ProgramFiles(x86)", str(kit_root))
    monkeypatch.setenv("ProgramData", str(vs_state_json))
    _patch_vs_root(monkeypatch, vs_root)
    paths = win_os.VisualStudioLayout.find_sdk_bin_paths()
    assert any(_SDK_VER in p and "x64" in p for p in paths)
    assert any(_SDK_VER in p and "x86" in p for p in paths)


def test_vs_layout_sdk_lib(vs_root, kit_root, vs_state_json, monkeypatch):
    monkeypatch.setenv("ProgramFiles(x86)", str(kit_root))
    monkeypatch.setenv("ProgramData", str(vs_state_json))
    _patch_vs_root(monkeypatch, vs_root)
    paths = win_os.VisualStudioLayout.find_sdk_lib_paths()
    assert any(_SDK_VER in p for p in paths)


def test_vs_layout_sdk_absent_without_state_json(vs_root, kit_root, tmp_path, monkeypatch):
    """SDK paths are empty when no VS instance state.json provides SDK version info."""
    empty_programdata = tmp_path / "ProgramData_empty"
    empty_programdata.mkdir()
    monkeypatch.setenv("ProgramFiles(x86)", str(kit_root))
    monkeypatch.setenv("ProgramData", str(empty_programdata))
    _patch_vs_root(monkeypatch, vs_root)
    assert win_os.VisualStudioLayout.find_sdk_bin_paths() == []
    assert win_os.VisualStudioLayout.find_sdk_lib_paths() == []


def test_vs_layout_wdk(kit_root, monkeypatch):
    monkeypatch.setenv("ProgramFiles(x86)", str(kit_root))
    monkeypatch.delenv("WDKContentRoot", raising=False)
    paths = win_os.VisualStudioLayout.find_wdk_paths()
    assert any("km" in p for p in paths)
    assert any(_SDK_VER in p for p in paths)


def test_vs_layout_wdk_absent(tmp_path, monkeypatch):
    """No km/ dirs in the kit tree yields an empty WDK list."""
    pf86 = tmp_path / "ProgramFiles86_no_wdk"
    kit_lib = pf86 / "Windows Kits" / "10" / "Lib"
    (kit_lib / _SDK_VER / "um" / "x64").mkdir(parents=True)
    monkeypatch.setenv("ProgramFiles(x86)", str(pf86))
    monkeypatch.delenv("WDKContentRoot", raising=False)
    assert win_os.VisualStudioLayout.find_wdk_paths() == []
