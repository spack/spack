# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
import collections
import os
import pathlib
import sys

import pytest

import spack.deptypes
import spack.detection
import spack.detection.common
import spack.detection.dependencies
import spack.detection.elf_closure
import spack.detection.ownership
import spack.detection.path
import spack.repo
import spack.spec
import spack.util.elf
import spack.util.filesystem
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


def _write_elf(path: pathlib.Path, **kwargs) -> str:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(spack.util.elf.minimal_elf(**kwargs))
    return str(path)


def _resolved(loaded, path: str):
    """Returns the real paths the DT_NEEDED entries of ``path`` resolve to."""
    return loaded[os.path.realpath(path)].needed


INTERPRETER = "/lib64/ld-linux-x86-64.so.2"


@pytest.mark.not_on_windows("ELF files are not loaded on Windows")
@pytest.mark.parametrize(
    "search_path,ld_library_path,expected",
    [
        # RPATH comes before LD_LIBRARY_PATH
        ({"rpath": "{tmp}/rpath"}, True, "rpath"),
        # LD_LIBRARY_PATH comes before RUNPATH
        ({"runpath": "{tmp}/runpath"}, True, "env"),
        ({"runpath": "{tmp}/runpath"}, False, "runpath"),
        # Default directories come last
        ({}, True, "env"),
        ({}, False, "default"),
    ],
)
def test_dynamic_loader_search_order(tmp_path, search_path, ld_library_path, expected):
    for directory in ("rpath", "env", "runpath", "default"):
        _write_elf(tmp_path / directory / "libz.so.1", soname="libz.so.1")
    kwargs = {k: v.format(tmp=tmp_path) for k, v in search_path.items()}
    exe = _write_elf(
        tmp_path / "bin" / "exe", needed=["libz.so.1"], interpreter=INTERPRETER, **kwargs
    )

    loader = spack.detection.elf_closure.DynamicLoader(
        ld_library_path=[str(tmp_path / "env")] if ld_library_path else [],
        default_dirs=[str(tmp_path / "default")],
    )
    loaded = loader.load(exe)

    assert _resolved(loaded, exe) == [os.path.realpath(tmp_path / expected / "libz.so.1")]


@pytest.mark.not_on_windows("ELF files are not loaded on Windows")
@pytest.mark.parametrize(
    "exe_search_path,lib_search_path,finds_libb",
    [
        # The RPATH of the loading file is searched for the libraries of what it loads
        ({"rpath": "{tmp}/lib"}, {}, True),
        # RUNPATH is used only for the DT_NEEDED entries of the file that has it
        ({"runpath": "{tmp}/lib"}, {}, False),
        # A file with a RUNPATH does not search the RPATH of the file that loaded it
        ({"rpath": "{tmp}/lib"}, {"runpath": "{tmp}/other"}, False),
    ],
)
def test_dynamic_loader_rpath_of_loading_files(
    tmp_path, exe_search_path, lib_search_path, finds_libb
):
    lib = tmp_path / "lib"
    _write_elf(
        lib / "liba.so",
        soname="liba.so",
        needed=["libb.so"],
        **{k: v.format(tmp=tmp_path) for k, v in lib_search_path.items()},
    )
    _write_elf(lib / "libb.so", soname="libb.so")
    exe = _write_elf(
        tmp_path / "bin" / "exe",
        needed=["liba.so"],
        interpreter=INTERPRETER,
        **{k: v.format(tmp=tmp_path) for k, v in exe_search_path.items()},
    )

    loader = spack.detection.elf_closure.DynamicLoader(ld_library_path=[], default_dirs=[])
    loaded = loader.load(exe)

    liba = loaded[os.path.realpath(lib / "liba.so")]
    if finds_libb:
        assert liba.needed == [os.path.realpath(lib / "libb.so")] and liba.missing == []
    else:
        assert liba.needed == [] and liba.missing == ["libb.so"]


@pytest.mark.not_on_windows("ELF files are not loaded on Windows")
def test_dynamic_loader_expands_origin(tmp_path):
    """Tests that $ORIGIN of an executable is its directory after resolving symlinks, and that
    $ORIGIN of a library is the directory it was found in, without resolving symlinks.
    """
    prefix = tmp_path / "prefix"
    store = tmp_path / "store"
    _write_elf(store / "liba.so", soname="liba.so", needed=["libb.so"], runpath="$ORIGIN/b")
    (prefix / "lib").mkdir(parents=True)
    (prefix / "lib" / "liba.so").symlink_to(store / "liba.so")
    _write_elf(prefix / "lib" / "b" / "libb.so", soname="libb.so")
    exe = _write_elf(
        prefix / "bin" / "exe",
        needed=["liba.so"],
        interpreter=INTERPRETER,
        runpath="${ORIGIN}/../lib",
    )
    link = tmp_path / "view" / "bin" / "exe"
    link.parent.mkdir(parents=True)
    link.symlink_to(exe)

    loader = spack.detection.elf_closure.DynamicLoader(ld_library_path=[], default_dirs=[])
    loaded = loader.load(str(link))

    assert set(loaded) == {
        os.path.realpath(exe),
        os.path.realpath(store / "liba.so"),
        os.path.realpath(prefix / "lib" / "b" / "libb.so"),
    }


@pytest.mark.not_on_windows("ELF files are not loaded on Windows")
def test_dynamic_loader_does_not_search_loaded_sonames(tmp_path):
    """Tests that a DT_NEEDED entry matching the soname of a loaded library resolves to that
    library, even when the requesting file would find another one.
    """
    _write_elf(tmp_path / "default" / "libz.so", soname="libz.so.1")
    _write_elf(tmp_path / "private" / "libz.so.1", soname="libz.so.1")
    _write_elf(
        tmp_path / "default" / "liba.so",
        soname="liba.so",
        needed=["libz.so.1"],
        runpath=str(tmp_path / "private"),
    )
    exe = _write_elf(
        tmp_path / "bin" / "exe", needed=["libz.so", "liba.so"], interpreter=INTERPRETER
    )

    loader = spack.detection.elf_closure.DynamicLoader(
        ld_library_path=[], default_dirs=[str(tmp_path / "default")]
    )
    loaded = loader.load(exe)

    default_libz = os.path.realpath(tmp_path / "default" / "libz.so")
    assert _resolved(loaded, str(tmp_path / "default" / "liba.so")) == [default_libz]
    assert os.path.realpath(tmp_path / "private" / "libz.so.1") not in loaded


@pytest.mark.not_on_windows("ELF files are not loaded on Windows")
def test_dynamic_loader_skips_incompatible_libraries(tmp_path):
    _write_elf(tmp_path / "lib32" / "libz.so.1", soname="libz.so.1", is_64_bit=False)
    (tmp_path / "script").mkdir()
    (tmp_path / "script" / "libz.so.1").write_text("INPUT(libz.so.1)")
    _write_elf(tmp_path / "lib64" / "libz.so.1", soname="libz.so.1")
    exe = _write_elf(tmp_path / "bin" / "exe", needed=["libz.so.1"], interpreter=INTERPRETER)

    loader = spack.detection.elf_closure.DynamicLoader(
        ld_library_path=[],
        default_dirs=[str(tmp_path / "lib32"), str(tmp_path / "script"), str(tmp_path / "lib64")],
    )
    loaded = loader.load(exe)

    assert _resolved(loaded, exe) == [os.path.realpath(tmp_path / "lib64" / "libz.so.1")]


@pytest.mark.not_on_windows("ELF files are not loaded on Windows")
def test_dynamic_loader_closure_with_cycle_and_missing_library(tmp_path):
    lib = tmp_path / "lib"
    _write_elf(lib / "liba.so", soname="liba.so", needed=["libb.so", "libmissing.so"])
    _write_elf(lib / "libb.so", soname="libb.so", needed=["liba.so"])

    loader = spack.detection.elf_closure.DynamicLoader(ld_library_path=[], default_dirs=[str(lib)])
    loaded = loader.load(str(lib / "liba.so"))

    liba, libb = os.path.realpath(lib / "liba.so"), os.path.realpath(lib / "libb.so")
    assert set(loaded) == {liba, libb}
    assert loaded[liba].needed == [libb] and loaded[liba].missing == ["libmissing.so"]
    assert loaded[libb].needed == [liba] and loaded[libb].missing == []


def test_dynamic_loader_root_not_elf(tmp_path):
    script = tmp_path / "script"
    script.write_text("#!/bin/sh\n")
    loader = spack.detection.elf_closure.DynamicLoader(ld_library_path=[], default_dirs=[])
    assert loader.load(str(script)) == {}
    assert loader.load(str(tmp_path / "does-not-exist")) == {}


@pytest.mark.not_on_windows("ELF files are not loaded on Windows")
def test_dynamic_loader_used_for_several_roots(tmp_path):
    """Tests that libraries resolved for one root do not affect the resolution for another."""
    for directory in ("first", "second"):
        _write_elf(tmp_path / directory / "libz.so.1", soname="libz.so.1")
    first = _write_elf(
        tmp_path / "bin" / "first",
        needed=["libz.so.1"],
        interpreter=INTERPRETER,
        rpath=str(tmp_path / "first"),
    )
    second = _write_elf(
        tmp_path / "bin" / "second",
        needed=["libz.so.1"],
        interpreter=INTERPRETER,
        rpath=str(tmp_path / "second"),
    )

    loader = spack.detection.elf_closure.DynamicLoader(ld_library_path=[], default_dirs=[])

    assert _resolved(loader.load(first), first) == [
        os.path.realpath(tmp_path / "first" / "libz.so.1")
    ]
    assert _resolved(loader.load(second), second) == [
        os.path.realpath(tmp_path / "second" / "libz.so.1")
    ]


@pytest.mark.not_on_windows("ELF files are not loaded on Windows")
def test_dynamic_loader_ignores_relative_ld_library_path_entries(tmp_path):
    """Tests that empty and relative entries in LD_LIBRARY_PATH, as in the split of an unset
    variable, do not resolve against the current working directory.
    """
    _write_elf(tmp_path / "cwd" / "libz.so.1", soname="libz.so.1")
    _write_elf(tmp_path / "cwd" / "lib" / "libz.so.1", soname="libz.so.1")
    _write_elf(tmp_path / "default" / "libz.so.1", soname="libz.so.1")
    exe = _write_elf(tmp_path / "bin" / "exe", needed=["libz.so.1"], interpreter=INTERPRETER)
    loader = spack.detection.elf_closure.DynamicLoader(
        ld_library_path=["", "lib"], default_dirs=[str(tmp_path / "default")]
    )

    with spack.util.filesystem.working_dir(tmp_path / "cwd"):
        loaded = loader.load(exe)

    assert _resolved(loaded, exe) == [os.path.realpath(tmp_path / "default" / "libz.so.1")]


@pytest.mark.not_on_windows("Uses shell scripts as mock executables")
def test_by_path_detailed_assigns_files_by_version(mock_executable, mock_packages):
    """Tests that when one directory yields several specs, each spec is detected from the files
    whose version matches its own.
    """
    gcc_12 = mock_executable("gcc-12", output="echo 12.3.0")
    gcc_13 = mock_executable("gcc-13", output="echo 13.2.0")
    # A file without a version belongs to no spec
    mock_executable("gcc", output="echo")

    detected = spack.detection.path.by_path_detailed(
        ["gcc"], repo=mock_packages, path_hints=[str(gcc_12.parent)]
    )

    files_by_version = {str(x.spec.versions): x.files for x in detected["gcc"]}
    assert files_by_version == {"12.3.0": [str(gcc_12)], "13.2.0": [str(gcc_13)]}


@pytest.mark.not_on_windows("Uses shell scripts as mock executables")
def test_detect_leaves_out_files_rejected_by_the_package(mock_executable, mock_packages):
    clang = mock_executable("clang", output="echo 'clang version 14.0.0'")
    clangxx = mock_executable("clang++", output="echo 'clang version 14.0.0'")
    clang_format = mock_executable("clang-format", output="echo 'clang version 14.0.0'")

    detected = spack.detection.path.ExecutablesFinder().detect(
        pkg=mock_packages.get_pkg_class("llvm"),
        paths=[str(clang), str(clangxx), str(clang_format)],
        repo_path=mock_packages,
    )

    assert [x.files for x in detected] == [[str(clang), str(clangxx)]]


def test_ownership_index_of_detectable_packages(mock_packages):
    """Tests that libraries are attributed through ``sonames``, falling back to ``libraries``,
    and executables through ``executables``, only for packages that can be detected.
    """
    index = spack.detection.ownership.ownership_index(mock_packages)

    # sonames-not-detectable sets the same sonames, but cannot be detected
    assert index.library_owners("libsonames-owner.so.1") == ["sonames-owner"]
    assert index.library_owners("liblibraries-owner.so.2") == ["libraries-owner"]
    assert index.library_owners("libunknown.so.1") == []

    assert index.executable_owners("sonames-owner") == ["sonames-owner"]
    assert index.executable_owners("mpichversion") == ["mpich"]
    assert index.executable_owners("libsonames-owner.so.1") == []


def _consumer_layout(tmp_path: pathlib.Path, needed_by_consumer_lib):
    """Creates an executable of sonames-consumer that loads ``libintermediate.so.1`` from its
    prefix, or ``libsonames-owner.so.1`` when ``needed_by_consumer_lib`` is None, and a library
    of sonames-owner in another prefix. Returns the executable.
    """
    owner_lib = tmp_path / "owner" / "lib"
    _write_elf(owner_lib / "libsonames-owner.so.1", soname="libsonames-owner.so.1")
    runpath = f"$ORIGIN/../lib:{owner_lib}"
    first = "libsonames-owner.so.1"
    if needed_by_consumer_lib is not None:
        first = needed_by_consumer_lib
        _write_elf(
            tmp_path / "consumer" / "lib" / first,
            soname=first,
            needed=["libsonames-owner.so.1"],
            runpath=str(owner_lib),
        )
    return _write_elf(
        tmp_path / "consumer" / "bin" / "sonames-consumer",
        needed=[first],
        interpreter=INTERPRETER,
        runpath=runpath,
    )


def _detect_dependencies(detected, externals, mock_packages):
    return spack.detection.dependencies.detect_dependencies(
        detected,
        externals=externals,
        index=spack.detection.ownership.ownership_index(mock_packages),
        loader=spack.detection.elf_closure.DynamicLoader(ld_library_path=[], default_dirs=[]),
        repo=mock_packages,
    )


@pytest.mark.not_on_windows("ELF files are not loaded on Windows")
@pytest.mark.parametrize(
    "intermediate,has_edge",
    [
        # The executable loads the library directly
        (None, True),
        # The search passes through libraries of no package, and of the package itself
        ("libhelper.so.1", True),
        ("libsonames-consumer.so.1", True),
        # The search stops at system libraries
        ("libstdc++.so.6", False),
    ],
)
def test_detect_dependencies_from_loaded_libraries(
    tmp_path, intermediate, has_edge, mock_packages, config
):
    exe = _consumer_layout(tmp_path, intermediate)
    consumer = spack.spec.Spec.from_detection(
        "sonames-consumer@1.0", external_path=str(tmp_path / "consumer")
    )
    owner = spack.spec.Spec.from_detection(
        "sonames-owner@1.0", external_path=str(tmp_path / "owner")
    )
    detected = [spack.detection.path.DetectedExternal(spec=consumer, files=[exe])]

    result = _detect_dependencies(detected, [consumer, owner], mock_packages)

    assert result.missing == []
    if not has_edge:
        assert result.edges == []
        return

    library = os.path.realpath(tmp_path / "owner" / "lib" / "libsonames-owner.so.1")
    assert result.edges == [
        spack.detection.dependencies.ExternalEdge(
            parent=consumer, child=owner, depflag=spack.deptypes.LINK, virtuals=(), library=library
        )
    ]


@pytest.mark.not_on_windows("ELF files are not loaded on Windows")
def test_detect_dependencies_without_external_in_prefix(tmp_path, mock_packages, config):
    """Tests that a library whose owner has no external in the prefix of the library is
    returned as missing.
    """
    exe = _consumer_layout(tmp_path, None)
    consumer = spack.spec.Spec.from_detection(
        "sonames-consumer@1.0", external_path=str(tmp_path / "consumer")
    )
    elsewhere = spack.spec.Spec.from_detection(
        "sonames-owner@1.0", external_path=str(tmp_path / "elsewhere")
    )
    detected = [spack.detection.path.DetectedExternal(spec=consumer, files=[exe])]

    result = _detect_dependencies(detected, [consumer, elsewhere], mock_packages)

    assert result.edges == []
    assert result.missing == [
        spack.detection.dependencies.MissingExternal(
            parent=consumer,
            library=os.path.realpath(tmp_path / "owner" / "lib" / "libsonames-owner.so.1"),
            owners=["sonames-owner"],
        )
    ]


@pytest.mark.not_on_windows("ELF files are not loaded on Windows")
def test_detect_dependencies_with_ambiguous_external(tmp_path, mock_packages, config):
    exe = _consumer_layout(tmp_path, None)
    consumer = spack.spec.Spec.from_detection(
        "sonames-consumer@1.0", external_path=str(tmp_path / "consumer")
    )
    owners = [
        spack.spec.Spec.from_detection(f"sonames-owner@{v}", external_path=str(tmp_path / "owner"))
        for v in ("1.0", "2.0")
    ]
    detected = [spack.detection.path.DetectedExternal(spec=consumer, files=[exe])]

    with pytest.warns(UserWarning, match="may belong to any of"):
        result = _detect_dependencies(detected, [consumer, *owners], mock_packages)

    assert result.edges == [] and result.missing == []


@pytest.mark.not_on_windows("ELF files are not loaded on Windows")
@pytest.mark.parametrize(
    "library,expected_version",
    [
        # The library is a symlink to a file whose name has the version
        ("liblibraries-owner.so.1", "1.0"),
        # The pattern of the recipe matches, but its version detection rejects the file
        ("liblibraries-owner-extra.so.1", None),
    ],
)
def test_detect_dependencies_on_package_detected_by_libraries(
    tmp_path, library, expected_version, mock_packages, config, recwarn
):
    """Tests that a package detected by its libraries owns only the libraries its recipe detects
    a version for, and that its externals are told apart by that version.
    """
    lib_dir = tmp_path / "usr" / "lib"
    real = _write_elf(lib_dir / f"{library}.0", soname=library)
    (lib_dir / library).symlink_to(real)
    exe = _write_elf(
        tmp_path / "consumer" / "bin" / "sonames-consumer",
        needed=[library],
        interpreter=INTERPRETER,
        runpath=str(lib_dir),
    )
    consumer = spack.spec.Spec.from_detection(
        "sonames-consumer@1.0", external_path=str(tmp_path / "consumer")
    )
    owners = {
        v: spack.spec.Spec.from_detection(
            f"libraries-owner@{v}", external_path=str(tmp_path / "usr")
        )
        for v in ("1.0", "2.0")
    }
    detected = [spack.detection.path.DetectedExternal(spec=consumer, files=[exe])]

    result = _detect_dependencies(detected, [consumer, *owners.values()], mock_packages)

    assert result.missing == [] and not recwarn.list
    if expected_version is None:
        assert result.edges == []
    else:
        assert [(x.child, x.library) for x in result.edges] == [
            (owners[expected_version], os.path.realpath(real))
        ]


@pytest.mark.not_on_windows("ELF files are not loaded on Windows")
def test_detect_dependencies_requires_link_dependency_in_recipe(tmp_path, mock_packages, config):
    """Tests that no edge is recorded when the recipe of the parent has only a build dependency
    on the owner of a library it loads.
    """
    exe = _consumer_layout(tmp_path, None)
    consumer = spack.spec.Spec.from_detection(
        "sonames-consumer@1.0~owner", external_path=str(tmp_path / "consumer")
    )
    owner = spack.spec.Spec.from_detection(
        "sonames-owner@1.0", external_path=str(tmp_path / "owner")
    )
    detected = [spack.detection.path.DetectedExternal(spec=consumer, files=[exe])]

    with pytest.warns(UserWarning, match="has no link dependency on sonames-owner"):
        result = _detect_dependencies(detected, [consumer, owner], mock_packages)

    assert result.edges == [] and result.missing == []


@pytest.mark.not_on_windows("ELF files are not loaded on Windows")
@pytest.mark.parametrize("layout", ["merged-usr", "view"])
def test_detect_dependencies_through_symlinks(tmp_path, layout, mock_packages, config):
    """Tests that a library is attributed to an external when either the path the library was
    found at, or its real path, is in the prefix of the external.
    """
    if layout == "merged-usr":
        # The library is found at <root>/lib, a symlink to <root>/usr/lib, and the prefix of
        # the external is <root>/usr
        real = _write_elf(
            tmp_path / "root" / "usr" / "lib" / "libsonames-owner.so.1",
            soname="libsonames-owner.so.1",
        )
        (tmp_path / "root" / "lib").symlink_to(tmp_path / "root" / "usr" / "lib")
        search_dir, prefix = tmp_path / "root" / "lib", tmp_path / "root" / "usr"
    else:
        # The library is found in a view, where it is a symlink to a file in another prefix,
        # and the prefix of the external is the view
        real = _write_elf(
            tmp_path / "store" / "lib" / "libsonames-owner.so.1", soname="libsonames-owner.so.1"
        )
        (tmp_path / "view" / "lib").mkdir(parents=True)
        (tmp_path / "view" / "lib" / "libsonames-owner.so.1").symlink_to(real)
        search_dir, prefix = tmp_path / "view" / "lib", tmp_path / "view"

    exe = _write_elf(
        tmp_path / "consumer" / "bin" / "sonames-consumer",
        needed=["libsonames-owner.so.1"],
        interpreter=INTERPRETER,
        runpath=str(search_dir),
    )
    consumer = spack.spec.Spec.from_detection(
        "sonames-consumer@1.0", external_path=str(tmp_path / "consumer")
    )
    owner = spack.spec.Spec.from_detection("sonames-owner@1.0", external_path=str(prefix))
    detected = [spack.detection.path.DetectedExternal(spec=consumer, files=[exe])]

    result = _detect_dependencies(detected, [consumer, owner], mock_packages)

    assert [(x.child, x.library) for x in result.edges] == [(owner, os.path.realpath(real))]
