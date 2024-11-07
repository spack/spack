# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import fnmatch
import os
import sys
from pathlib import Path

import pytest

import spack.paths
from spack.llnl.util.filesystem import HeaderList, LibraryList, find_headers, find_libraries


@pytest.fixture()
def library_list():
    """Returns an instance of LibraryList."""
    # Test all valid extensions: ['.a', '.dylib', '.so']
    libs = (
        [
            "/dir1/liblapack.a",
            "/dir2/libpython3.6.dylib",  # name may contain periods
            "/dir1/libblas.a",
            "/dir3/libz.so",
            "libmpi.so.20.10.1",  # shared object libraries may be versioned
        ]
        if sys.platform != "win32"
        else [
            "/dir1/liblapack.lib",
            "/dir2/libpython3.6.dll",
            "/dir1/libblas.lib",
            "/dir3/libz.dll",
            "libmpi.dll.20.10.1",
        ]
    )

    return LibraryList(libs)


@pytest.fixture()
def header_list():
    """Returns an instance of header list"""
    # Test all valid extensions: ['.h', '.hpp', '.hh', '.cuh']
    headers = [
        "/dir1/Python.h",
        "/dir2/date.time.h",
        "/dir1/pyconfig.hpp",
        "/dir3/core.hh",
        "pymem.cuh",
    ]
    h = HeaderList(headers)
    h.add_macro("-DBOOST_LIB_NAME=boost_regex")
    h.add_macro("-DBOOST_DYN_LINK")
    return h


# TODO: Remove below when spack.llnl.util.filesystem.find_libraries becomes spec aware
plat_static_ext = "lib" if sys.platform == "win32" else "a"


plat_shared_ext = "dll" if sys.platform == "win32" else "so"


plat_apple_shared_ext = "dylib"


class TestLibraryList:
    def test_repr(self, library_list):
        x = eval(repr(library_list))
        assert library_list == x

    def test_joined_and_str(self, library_list):
        s1 = library_list.joined()
        expected = " ".join(
            [
                "/dir1/liblapack.%s" % plat_static_ext,
                "/dir2/libpython3.6.%s"
                % (plat_apple_shared_ext if sys.platform != "win32" else "dll"),
                "/dir1/libblas.%s" % plat_static_ext,
                "/dir3/libz.%s" % plat_shared_ext,
                "libmpi.%s.20.10.1" % plat_shared_ext,
            ]
        )
        assert s1 == expected

        s2 = str(library_list)
        assert s1 == s2

        s3 = library_list.joined(";")
        expected = ";".join(
            [
                "/dir1/liblapack.%s" % plat_static_ext,
                "/dir2/libpython3.6.%s"
                % (plat_apple_shared_ext if sys.platform != "win32" else "dll"),
                "/dir1/libblas.%s" % plat_static_ext,
                "/dir3/libz.%s" % plat_shared_ext,
                "libmpi.%s.20.10.1" % plat_shared_ext,
            ]
        )
        assert s3 == expected

    def test_flags(self, library_list):
        search_flags = library_list.search_flags
        assert "-L/dir1" in search_flags
        assert "-L/dir2" in search_flags
        assert "-L/dir3" in search_flags
        assert isinstance(search_flags, str)
        assert search_flags == "-L/dir1 -L/dir2 -L/dir3"

        link_flags = library_list.link_flags
        assert "-llapack" in link_flags
        assert "-lpython3.6" in link_flags
        assert "-lblas" in link_flags
        assert "-lz" in link_flags
        assert "-lmpi" in link_flags
        assert isinstance(link_flags, str)
        assert link_flags == "-llapack -lpython3.6 -lblas -lz -lmpi"

        ld_flags = library_list.ld_flags
        assert isinstance(ld_flags, str)
        assert ld_flags == search_flags + " " + link_flags

    def test_paths_manipulation(self, library_list):
        names = library_list.names
        assert names == ["lapack", "python3.6", "blas", "z", "mpi"]

        directories = library_list.directories
        assert directories == ["/dir1", "/dir2", "/dir3"]

    def test_get_item(self, library_list):
        a = library_list[0]
        assert a == "/dir1/liblapack.%s" % plat_static_ext

        b = library_list[:]
        assert type(b) is type(library_list)
        assert library_list == b
        assert library_list is not b

    def test_add(self, library_list):
        pylist = [
            "/dir1/liblapack.%s" % plat_static_ext,  # removed from the final list
            "/dir2/libmpi.%s" % plat_shared_ext,
            "/dir4/libnew.%s" % plat_static_ext,
        ]
        another = LibraryList(pylist)
        both = library_list + another
        assert len(both) == 7

        # Invariant
        assert both == both + both

        # Always produce an instance of LibraryList
        assert type(library_list + pylist) is type(library_list)
        assert type(pylist + library_list) is type(library_list)


class TestHeaderList:
    def test_repr(self, header_list):
        x = eval(repr(header_list))
        assert header_list == x

    def test_joined_and_str(self, header_list):
        s1 = header_list.joined()
        expected = " ".join(
            [
                "/dir1/Python.h",
                "/dir2/date.time.h",
                "/dir1/pyconfig.hpp",
                "/dir3/core.hh",
                "pymem.cuh",
            ]
        )
        assert s1 == expected

        s2 = str(header_list)
        assert s1 == s2

        s3 = header_list.joined(";")
        expected = ";".join(
            [
                "/dir1/Python.h",
                "/dir2/date.time.h",
                "/dir1/pyconfig.hpp",
                "/dir3/core.hh",
                "pymem.cuh",
            ]
        )
        assert s3 == expected

    def test_flags(self, header_list):
        include_flags = header_list.include_flags
        assert "-I/dir1" in include_flags
        assert "-I/dir2" in include_flags
        assert "-I/dir3" in include_flags
        assert isinstance(include_flags, str)
        assert include_flags == "-I/dir1 -I/dir2 -I/dir3"

        macros = header_list.macro_definitions
        assert "-DBOOST_LIB_NAME=boost_regex" in macros
        assert "-DBOOST_DYN_LINK" in macros
        assert isinstance(macros, str)
        assert macros == "-DBOOST_LIB_NAME=boost_regex -DBOOST_DYN_LINK"

        cpp_flags = header_list.cpp_flags
        assert isinstance(cpp_flags, str)
        assert cpp_flags == include_flags + " " + macros

    def test_paths_manipulation(self, header_list):
        names = header_list.names
        assert names == ["Python", "date.time", "pyconfig", "core", "pymem"]

        directories = header_list.directories
        assert directories == ["/dir1", "/dir2", "/dir3"]

    def test_get_item(self, header_list):
        a = header_list[0]
        assert a == "/dir1/Python.h"

        b = header_list[:]
        assert type(b) is type(header_list)
        assert header_list == b
        assert header_list is not b

    def test_add(self, header_list):
        pylist = [
            "/dir1/Python.h",  # removed from the final list
            "/dir2/pyconfig.hpp",
            "/dir4/date.time.h",
        ]
        another = HeaderList(pylist)
        h = header_list + another
        assert len(h) == 7

        # Invariant : l == l + l
        assert h == h + h

        # Always produce an instance of HeaderList
        assert type(header_list + pylist) is type(header_list)
        assert type(pylist + header_list) is type(header_list)


#: Directory where the data for the test below is stored
search_dir = os.path.join(spack.paths.test_path, "data", "directory_search")


@pytest.mark.parametrize(
    "lib_list,kwargs",
    [
        (["liba"], {"shared": True, "recursive": True}),
        (["liba"], {"shared": False, "recursive": True}),
        (["libc", "liba"], {"shared": True, "recursive": True}),
        (["liba", "libc"], {"shared": False, "recursive": True}),
        (["libc", "libb", "liba"], {"shared": True, "recursive": True}),
        (["liba", "libb", "libc"], {"shared": False, "recursive": True}),
    ],
)
def test_library_type_search(lib_list, kwargs):
    results = find_libraries(lib_list, search_dir, **kwargs)
    assert len(results) != 0
    for result in results:
        lib_type_ext = plat_shared_ext
        if not kwargs["shared"]:
            lib_type_ext = plat_static_ext
        assert result.endswith(lib_type_ext) or (
            kwargs["shared"] and result.endswith(plat_apple_shared_ext)
        )


@pytest.mark.parametrize(
    "search_fn,search_list,root,kwargs",
    [
        (find_libraries, "liba", search_dir, {"recursive": True}),
        (find_libraries, ["liba"], search_dir, {"recursive": True}),
        (find_libraries, "libb", search_dir, {"recursive": True}),
        (find_libraries, ["libc"], search_dir, {"recursive": True}),
        (find_libraries, ["libc", "liba"], search_dir, {"recursive": True}),
        (find_libraries, ["liba", "libc"], search_dir, {"recursive": True}),
        (find_libraries, ["libc", "libb", "liba"], search_dir, {"recursive": True}),
        (find_libraries, ["liba", "libc"], search_dir, {"recursive": True}),
        (
            find_libraries,
            ["libc", "libb", "liba"],
            search_dir,
            {"recursive": True, "shared": False},
        ),
        (find_headers, "a", search_dir, {"recursive": True}),
        (find_headers, ["a"], search_dir, {"recursive": True}),
        (find_headers, "b", search_dir, {"recursive": True}),
        (find_headers, ["c"], search_dir, {"recursive": True}),
        (find_headers, ["c", "a"], search_dir, {"recursive": True}),
        (find_headers, ["a", "c"], search_dir, {"recursive": True}),
        (find_headers, ["c", "b", "a"], search_dir, {"recursive": True}),
        (find_headers, ["a", "c"], search_dir, {"recursive": True}),
        # recursive=False is the default
        (find_libraries, ["liba", "libd"], os.path.join(search_dir, "lib", "a"), {}),
        (find_headers, ["b", "d"], os.path.join(search_dir, "include", "a"), {}),
    ],
)
def test_searching_order(search_fn, search_list, root, kwargs):
    """Tests whether when multiple libraries or headers are searched for, like [a, b], the found
    file list adheres to the same ordering: [a matches..., b matches...], which is relevant in case
    of dependencies across static libraries, and we want to ensure they are passed in the correct
    order to the linker."""
    # Test search
    result = search_fn(search_list, root, **kwargs)

    # The tests are set-up so that something is always found
    assert len(result) != 0

    # Now reverse the result and start discarding things
    # as soon as you have matches. In the end the list should
    # be emptied.
    rlist = list(reversed(result))

    # At this point make sure the search list is a sequence
    if isinstance(search_list, str):
        search_list = [search_list]

    # Discard entries in the order they appear in search list
    for x in search_list:
        try:
            while fnmatch.fnmatch(rlist[-1], x) or x in rlist[-1]:
                rlist.pop()
        except IndexError:
            # List is empty
            pass

    # List should be empty here
    assert len(rlist) == 0


class TestLibrariesHeuristicStrategy:
    """Test the heuristic strategy for find_libraries"""

    def test_heuristic_finds_libraries_in_root_and_common_lib_dirs(self, tmp_path: Path):
        """Test that heuristic finds libraries in root/*, root/lib/*, root/lib64/* without
        recursion, but NOT in deeper levels like root/lib64/private/*."""

        # Create directory structure
        root = tmp_path / "test_root"
        root.mkdir()

        # Create lib directories
        lib_dir = root / "lib"
        lib64_dir = root / "lib64"
        lib_dir.mkdir()
        lib64_dir.mkdir()

        # Create deeper directory that should NOT be found with early return
        private_dir = lib64_dir / "private"
        private_dir.mkdir()

        # Create test libraries
        (root / f"libroot.{plat_shared_ext}").touch()
        (lib_dir / f"libinlib.{plat_shared_ext}").touch()
        (lib64_dir / f"libinlib64.{plat_shared_ext}").touch()
        (private_dir / f"libprivate.{plat_shared_ext}").touch()  # Should NOT be found

        # Test that heuristic finds the shallow libraries but not the deep ones
        result = find_libraries(
            ["libroot", "libinlib", "libinlib64", "libprivate"], str(root), strategy="heuristic"
        )

        # Should find the shallow ones, NOT the deep one due to early return
        assert len(result) == 3
        assert {os.path.basename(lib) for lib in result} == {
            f"libroot.{plat_shared_ext}",
            f"libinlib.{plat_shared_ext}",
            f"libinlib64.{plat_shared_ext}",
        }

    def test_heuristic_finds_at_triplet_level_but_not_non_lib_dirs(self, tmp_path: Path):
        """Test that heuristic finds libraries at root/lib/*/* and root/lib64/*/*
        but NOT in non-lib directories like root/foo/*."""

        root = tmp_path / "test_root"
        root.mkdir()

        # Create lib directories with triplet subdirs
        lib_dir = root / "lib"
        lib64_dir = root / "lib64"
        foo_dir = root / "foo"  # Not a common lib dir
        lib_dir.mkdir()
        lib64_dir.mkdir()
        foo_dir.mkdir()

        triplet_lib = lib_dir / "x86_64-linux-gnu"
        triplet_lib64 = lib64_dir / "x86_64-linux-gnu"
        triplet_foo = foo_dir / "x86_64-linux-gnu"
        triplet_lib.mkdir()
        triplet_lib64.mkdir()
        triplet_foo.mkdir()

        # Create libraries - only the ones in lib/* and lib64/* should be found
        (triplet_lib / f"libtriplet.{plat_shared_ext}").touch()
        (triplet_lib64 / f"libtriplet64.{plat_shared_ext}").touch()
        (triplet_foo / f"libfoo.{plat_shared_ext}").touch()  # Should NOT be found

        # No libraries in root or direct lib dirs, so it goes to second heuristic level
        result = find_libraries(
            ["libtriplet", "libtriplet64", "libfoo"], str(root), strategy="heuristic"
        )

        # Should find in lib/* and lib64/* only
        assert len(result) == 2
        assert {os.path.basename(lib) for lib in result} == {
            f"libtriplet.{plat_shared_ext}",
            f"libtriplet64.{plat_shared_ext}",
        }

    def test_heuristic_does_not_find_deep_libraries_with_default_max_depth(self, tmp_path: Path):
        """Test that heuristic does NOT find libraries at root/lib/*/*/* with default max_depth."""

        root = tmp_path / "test_root"
        root.mkdir()

        # Create deep directory structure
        lib_dir = root / "lib"
        lib_dir.mkdir()

        # Create 3-level deep directory
        level2 = lib_dir / "level2"
        level3 = level2 / "level3"
        level2.mkdir()
        level3.mkdir()

        # Put library only at the deepest level (3 levels under root)
        (level3 / f"libdeep.{plat_shared_ext}").touch()

        # With default max_depth=2, this should NOT be found
        assert not find_libraries(["libdeep"], str(root), strategy="heuristic")

        # With sufficient max_depth, it should be found
        result = find_libraries(["libdeep"], str(root), strategy="heuristic", max_depth=3)
        assert {os.path.basename(lib) for lib in result} == {f"libdeep.{plat_shared_ext}"}

    def test_heuristic_early_return_behavior(self, tmp_path: Path):
        """Test that heuristic returns early when libraries are found at shallow levels."""

        root = tmp_path / "test_root"
        root.mkdir()

        # Create directory structure
        lib_dir = root / "lib"
        lib_dir.mkdir()

        triplet_dir = lib_dir / "x86_64-linux-gnu"
        deep_dir = triplet_dir / "deep"
        triplet_dir.mkdir()
        deep_dir.mkdir()

        # Create same-named library at multiple levels
        (root / f"libtest.{plat_shared_ext}").touch()  # Shallow (should be found first)
        (triplet_dir / f"libtest.{plat_shared_ext}").touch()  # Deeper (should not be reached)
        (deep_dir / f"libtest.{plat_shared_ext}").touch()  # Deepest (should not be reached)

        result = find_libraries(["libtest"], str(root), strategy="heuristic")

        # Should find exactly one (the shallow one) due to early return
        assert len(result) == 1
        assert result[0] == str(root / f"libtest.{plat_shared_ext}")

    def test_heuristic_when_root_is_lib_directory(self, tmp_path: Path):
        """Test heuristic behavior when root itself is a common lib directory."""

        # Create a lib directory as root
        lib_root = tmp_path / "lib"
        lib_root.mkdir()

        # Create subdirectories
        level1_dir = lib_root / "level1"
        level2_dir = level1_dir / "level2"
        level3_dir = level2_dir / "level3"
        level1_dir.mkdir()
        level2_dir.mkdir()
        level3_dir.mkdir()

        # Test case 1: Library only in root
        (lib_root / f"libroot.{plat_shared_ext}").touch()
        result1 = find_libraries(["libroot"], str(lib_root), strategy="heuristic")
        assert len(result1) == 1
        assert {os.path.basename(lib) for lib in result1} == {f"libroot.{plat_shared_ext}"}

        # Clean up for next test
        (lib_root / f"libroot.{plat_shared_ext}").unlink()

        # Test case 2: Library at level 1. Should be found.
        (level1_dir / f"liblevel1.{plat_shared_ext}").touch()
        result2 = find_libraries(["liblevel1"], str(lib_root), strategy="heuristic")
        assert len(result2) == 1
        assert {os.path.basename(lib) for lib in result2} == {f"liblevel1.{plat_shared_ext}"}

        # Test case 3: Library at level 3. Should NOT be found with default max_depth=2
        (level3_dir / f"liblevel3.{plat_shared_ext}").touch()
        result3 = find_libraries(["liblevel3"], str(lib_root), strategy="heuristic")
        assert len(result3) == 0

        # Test case 4: Same library should be found with increased max_depth
        result4 = find_libraries(["liblevel3"], str(lib_root), strategy="heuristic", max_depth=3)
        assert len(result4) == 1
        assert {os.path.basename(lib) for lib in result4} == {f"liblevel3.{plat_shared_ext}"}

    def test_heuristic_no_libraries_found(self, tmp_path: Path):
        """Test that heuristic returns empty list when no libraries are found."""
        root = tmp_path / "empty_root"
        root.mkdir()

        # Create lib directories but no libraries
        lib_dir = root / "lib"
        lib64_dir = root / "lib64"
        lib_dir.mkdir()
        lib64_dir.mkdir()

        result = find_libraries(["nonexistent"], str(root), strategy="heuristic")
        assert isinstance(result, LibraryList) and not result

    @pytest.mark.skipif(sys.platform == "win32", reason="Test focuses on Unix lib dirs")
    def test_heuristic_unix_lib_directories_only(self, tmp_path: Path):
        """Test that heuristic only considers lib and lib64 on Unix systems."""

        root = tmp_path / "test_root"
        root.mkdir()

        # Create various directories. Only lib and lib64 should be searched
        for dirname in ["lib", "lib64", "bin", "share", "include"]:
            dir_path = root / dirname
            dir_path.mkdir()
            (dir_path / f"lib{dirname}.{plat_shared_ext}").touch()

        # On Unix, only lib and lib64 are considered common lib dirs
        result = find_libraries(
            [f"lib{d}" for d in ["lib", "lib64", "bin", "share", "include"]],
            str(root),
            strategy="heuristic",
        )

        # Should find only in lib and lib64
        assert len(result) == 2
        assert {os.path.basename(lib) for lib in result} == {
            f"liblib.{plat_shared_ext}",
            f"liblib64.{plat_shared_ext}",
        }


class TestHeadersHeuristicStrategy:
    """Test the heuristic strategy for find_headers."""

    def test_heuristic_redirects_to_include_directory(self, tmp_path: Path):
        """Test that heuristic automatically redirects to <root>/include when root is not an
        include dir."""

        root = tmp_path / "test_root"
        root.mkdir()

        # Create include directory
        include_dir = root / "include"
        include_dir.mkdir()

        # Create some other directories that should be ignored
        lib_dir = root / "lib"
        bin_dir = root / "bin"
        lib_dir.mkdir()
        bin_dir.mkdir()

        # Place headers in include directory and other places
        (include_dir / "test.h").touch()
        (lib_dir / "ignored.h").touch()  # Should be ignored
        (bin_dir / "ignored2.h").touch()  # Should be ignored

        # Test that heuristic finds the header in include but not elsewhere
        result = find_headers(["test", "ignored", "ignored2"], str(root), strategy="heuristic")

        # Should find header in include directory
        assert len(result) == 1
        assert {os.path.basename(h) for h in result} == {"test.h"}

    def test_heuristic_works_when_root_is_include_directory(self, tmp_path: Path):
        """Test heuristic behavior when root itself is already an include directory."""

        # Create an include directory as root
        include_root = tmp_path / "include"
        include_root.mkdir()

        # Create subdirectories
        subdir1 = include_root / "subdir1"
        subdir2 = subdir1 / "subdir2"
        subdir3 = subdir2 / "subdir3"
        subdir1.mkdir()
        subdir2.mkdir()
        subdir3.mkdir()

        # Create headers at different levels
        (include_root / "level0.h").touch()  # depth 0
        (subdir1 / "level1.h").touch()  # depth 1
        (subdir2 / "level2.h").touch()  # depth 2
        (subdir3 / "level3.h").touch()  # depth 3

        # Test with default max_depth=3, should find up to level 3
        result = find_headers(
            ["level0", "level1", "level2", "level3"], str(include_root), strategy="heuristic"
        )

        # Should find all headers within max_depth=3
        assert len(result) == 4
        assert {os.path.basename(header) for header in result} == {
            "level0.h",
            "level1.h",
            "level2.h",
            "level3.h",
        }

    def test_heuristic_respects_max_depth(self, tmp_path: Path):
        """Test that heuristic respects custom max_depth parameter."""

        root = tmp_path / "test_root"
        root.mkdir()

        include_dir = root / "include"
        include_dir.mkdir()

        # Create nested structure
        level2 = include_dir / "level2"
        level3 = level2 / "level3"
        level4 = level3 / "level4"
        level2.mkdir()
        level3.mkdir()
        level4.mkdir()

        # Place headers at different depths from include directory
        (level2 / "shallow.h").touch()
        (level3 / "medium.h").touch()
        (level4 / "deep.h").touch()

        result = find_headers(
            ["shallow", "medium", "deep"], str(root), strategy="heuristic", max_depth=2
        )

        # Should find shallow header (within max_depth)
        assert len(result) == 1
        assert {os.path.basename(header) for header in result} == {"shallow.h"}

        # Test with higher max_depth=4. Should find all
        result2 = find_headers(
            ["shallow", "medium", "deep"], str(root), strategy="heuristic", max_depth=4
        )
        assert len(result2) == 3
        assert {os.path.basename(header) for header in result2} == {
            "shallow.h",
            "medium.h",
            "deep.h",
        }

    def test_heuristic_finds_multiple_header_extensions(self, tmp_path: Path):
        """Test that heuristic finds headers with different extensions."""

        root = tmp_path / "test_root"
        root.mkdir()

        include_dir = root / "include"
        include_dir.mkdir()

        # Create headers with different extensions
        (include_dir / "test.h").touch()  # C header
        (include_dir / "test.hpp").touch()  # C++ header
        (include_dir / "test.hxx").touch()  # C++ header
        (include_dir / "test.hh").touch()  # C++ header

        # Search for the base name - should find all extensions
        result = find_headers(["test"], str(root), strategy="heuristic")

        # Should find all the different extensions
        assert len(result) == 4
        assert {os.path.basename(header) for header in result} == {
            "test.h",
            "test.hpp",
            "test.hxx",
            "test.hh",
        }

    def test_heuristic_detects_existing_include_in_path(self, tmp_path: Path):
        """Test that heuristic detects when root path already contains 'include'."""

        # Create a path that already has 'include' in the last 3 parts
        base_dir = tmp_path / "prefix"
        include_dir = base_dir / "include"
        subdir = include_dir / "subdir"
        base_dir.mkdir()
        include_dir.mkdir()
        subdir.mkdir()

        # Create a header in the subdirectory
        (subdir / "existing.h").touch()

        # Test with root being the include directory - should not redirect further
        result = find_headers(["existing"], str(include_dir), strategy="heuristic")

        assert len(result) == 1
        assert os.path.basename(result[0]) == "existing.h"

        # Test with root being a subdirectory of include - should not redirect
        result2 = find_headers(["existing"], str(subdir), strategy="heuristic")

        assert len(result2) == 1
        assert os.path.basename(result2[0]) == "existing.h"

    def test_heuristic_no_headers_found(self, tmp_path: Path):
        """Test that heuristic returns empty list when no headers are found."""

        root = tmp_path / "empty_root"
        root.mkdir()

        # Create include directory but no headers
        include_dir = root / "include"
        include_dir.mkdir()

        result = find_headers(["nonexistent"], str(root), strategy="heuristic")
        assert isinstance(result, HeaderList) and not result
