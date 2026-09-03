# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
import collections
import pathlib

import spack.detection
import spack.detection.common
import spack.detection.path
import spack.spec
from spack.config import Configuration


def test_detection_update_config(mutable_config: Configuration):
    # mock detected package
    detected_packages = collections.defaultdict(list)
    detected_packages["cmake"] = [spack.spec.Spec("cmake@3.27.5", external_path="/usr/bin")]

    # update config for new package
    spack.detection.common.update_configuration(detected_packages)
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
