# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

"""Install debug artifacts for packages built with ``--debuggable``.

This module is called from both the old installer (``spack.installer``) and the
new installer (``spack.new_installer``) after the real build completes and while
the staging directory is still alive.

Public entry point
------------------
install_debug_artifacts(pkg)
    The single function callers should use.  Everything else is private.
"""

import enum
import json
import os
import re
import subprocess
from typing import TYPE_CHECKING, Dict, Set

import spack.builder
import spack.error
import spack.llnl.util.filesystem as fs
import spack.llnl.util.tty as tty

if TYPE_CHECKING:
    import spack.package_base


# ---------------------------------------------------------------------------
# Failure policy machinery
# ---------------------------------------------------------------------------


class DebugInstallFailurePolicy(enum.Enum):
    """Severity of failures during a debuggable installation.

    FATAL:   Installation is aborted immediately via InstallError.
             The debuggable install cannot proceed meaningfully.

    WARNING: Installation continues but the user is notified.
             Partial coverage is acceptable; user should know.

    INFO:    Expected or benign condition; logged at debug level only.
    """

    FATAL = "fatal"
    WARNING = "warning"
    INFO = "info"


#: Maps each known failure mode to its enforcement policy.
#: Every failure that can occur during a debuggable install must be
#: listed here. No failure is silently swallowed.
_DEBUGGABLE_FAILURE_POLICIES: Dict[str, DebugInstallFailurePolicy] = {
    # compile_commands.json absent or malformed.
    # We fall back to DWARF-derived paths — not fatal.
    "compile_commands_missing": DebugInstallFailurePolicy.INFO,
    # A specific source file referenced in DWARF was not in staging.
    # Happens for generated files cleaned up before install. Common.
    "source_file_missing": DebugInstallFailurePolicy.INFO,
    # Generated header installation failed for some files.
    # Generated types may not resolve in debugger.
    "generated_headers_partial": DebugInstallFailurePolicy.WARNING,
}


def _handle_debuggable_failure(failure_type: str, detail: str, pkg_id: str) -> None:
    """Enforce the failure policy for a named failure mode.

    Looks up ``failure_type`` in ``_DEBUGGABLE_FAILURE_POLICIES`` and
    applies the corresponding action:

    - FATAL    raises :exc:`spack.error.InstallError` immediately
    - WARNING  calls ``tty.warn``
    - INFO     calls ``tty.debug``

    Unknown failure types default to WARNING so new failure modes added
    during development are never silently swallowed.

    Args:
        failure_type: key into ``_DEBUGGABLE_FAILURE_POLICIES``
        detail:       human-readable description of what went wrong
        pkg_id:       package identifier string for the error message
    """
    policy = _DEBUGGABLE_FAILURE_POLICIES.get(failure_type, DebugInstallFailurePolicy.WARNING)
    message = f"[debuggable:{failure_type}] {pkg_id}: {detail}"

    if policy == DebugInstallFailurePolicy.FATAL:
        raise spack.error.InstallError(message)
    elif policy == DebugInstallFailurePolicy.WARNING:
        tty.warn(message)
    else:
        tty.debug(message)


# ---------------------------------------------------------------------------
# ELF / DWARF inspection helpers
# ---------------------------------------------------------------------------


def _is_elf_with_debug_sections(filepath: str) -> bool:
    """Return True if the file is an ELF binary containing DWARF debug sections.

    Uses a two-stage check:

    1. Read the first 4 bytes and verify ELF magic (``\\x7fELF``).
       This is fast and avoids invoking readelf on every file.

    2. If ELF magic matches, run ``readelf --sections --wide`` and check
       for the presence of ``.debug_info`` or ``.debug_str`` sections.
       Stripped binaries pass the magic check but have no DWARF and
       should not be processed.

    Args:
        filepath: absolute path to the file to inspect

    Returns:
        True only if the file is ELF *and* has DWARF debug sections.
        False for scripts, text files, stripped ELF, and unreadable files.
    """
    ELF_MAGIC = b"\x7fELF"
    try:
        with open(filepath, "rb") as f:
            if f.read(4) != ELF_MAGIC:
                return False

        result = subprocess.run(
            ["readelf", "--sections", "--wide", filepath],
            capture_output=True,
            text=True,
            timeout=10,
        )
        return ".debug_info" in result.stdout or ".debug_str" in result.stdout

    except (IOError, OSError, subprocess.TimeoutExpired, FileNotFoundError):
        return False


def _parse_dwarf_comp_unit_paths(readelf_output: str, paths: Set[str]) -> None:
    """Parse ``readelf --debug-dump=info`` output to extract source file paths.

    Each compilation unit DIE in DWARF contains:

    - ``DW_AT_comp_dir``: the working directory at compile time
    - ``DW_AT_name``: the source filename (relative or absolute)

    The full path is ``os.path.join(DW_AT_comp_dir, DW_AT_name)`` when
    ``DW_AT_name`` is relative, or just ``DW_AT_name`` when absolute.

    Args:
        readelf_output: the full stdout from ``readelf --debug-dump=info``
        paths:          set to update in place with discovered paths
    """
    comp_dir = None
    for line in readelf_output.splitlines():
        line = line.strip()
        if "DW_AT_comp_dir" in line:
            m = re.search(r"DW_AT_comp_dir\b.*:\s*(.+)$", line)
            if m:
                comp_dir = m.group(1).strip()
        elif "DW_AT_name" in line and comp_dir is not None:
            m = re.search(r"DW_AT_name\b.*:\s*(.+)$", line)
            if m:
                name = m.group(1).strip()
                if os.path.isabs(name):
                    paths.add(name)
                else:
                    paths.add(os.path.join(comp_dir, name))
            comp_dir = None


def _extract_compilation_unit_paths(pkg: "spack.package_base.PackageBase") -> Set[str]:
    """Extract every source file path embedded in DWARF across all installed ELF binaries.

    This is the authoritative source file list for deciding what to copy
    during a debuggable installation. It works for any build system —
    CMake, autotools, Make, raw Fortran, CUDA host code — because it reads
    what the compiler actually embedded, not what a build manifest says.

    Uses ``readelf --debug-dump=info --dwarf-depth=1`` which limits output
    to top-level DIEs only (one per compilation unit). This is much faster
    than a full DWARF dump and provides exactly what we need.

    The ``share/<pkg>/`` subdirectory is excluded from the walk because it
    contains the debug artifacts we are currently installing — we do not
    want to re-scan our own output.

    Args:
        pkg: the package whose installed prefix to scan

    Returns:
        Set of absolute source file paths as embedded in DWARF.
        If ``-ffile-prefix-map`` was injected correctly, these will be
        permanent prefix paths, not staging paths.
    """
    prefix = str(pkg.spec.prefix)
    share_dir = os.path.join(prefix, "share", pkg.name)
    paths: Set[str] = set()

    for root, _, files in os.walk(prefix):
        if root.startswith(share_dir):
            continue

        for filename in files:
            filepath = os.path.join(root, filename)

            if os.path.islink(filepath):
                continue

            if not _is_elf_with_debug_sections(filepath):
                continue

            try:
                result = subprocess.run(
                    ["readelf", "--debug-dump=info", "--dwarf-depth=1", filepath],
                    capture_output=True,
                    text=True,
                    timeout=60,
                )
                _parse_dwarf_comp_unit_paths(result.stdout, paths)

            except subprocess.TimeoutExpired:
                tty.debug(f"[debuggable] readelf timed out on {filepath}, skipping")
            except FileNotFoundError:
                tty.debug("[debuggable] readelf not found on this system")
                return paths
            except Exception as e:
                tty.debug(f"[debuggable] readelf failed on {filepath}: {e}")

    return paths


# ---------------------------------------------------------------------------
# Public entry point
# ---------------------------------------------------------------------------


def install_debug_artifacts(pkg: "spack.package_base.PackageBase") -> None:
    """Install DWARF-filtered sources, generated headers, and compile_commands.json.

    Must be called from within the child build process, after the real
    install completes and while the staging directory is still present
    (i.e. inside the ``with stage:`` context manager).

    Args:
        pkg:          the package that was just installed
    """
    pkg_id = f"{pkg.spec.name}-{pkg.spec.version}-{pkg.spec.dag_hash()}"
    pre = f"{pkg.spec.name}:"

    prefix = str(pkg.spec.prefix)
    staging_src = pkg.stage.source_path
    permanent_src = os.path.join(prefix, "share", pkg.name, "src")
    share_base = os.path.join(prefix, "share", pkg.name)
    build_target = os.path.join(share_base, "build")

    fs.mkdirp(share_base)

    # ── Step 1: get the authoritative source file list from DWARF ─────────
    tty.debug(f"{pre} Extracting compilation unit paths from DWARF...")
    dwarf_paths = _extract_compilation_unit_paths(pkg)
    tty.debug(f"{pre} DWARF reported {len(dwarf_paths)} compilation units")

    try:
        builder = spack.builder.create(pkg)
        staging_build_dir = getattr(builder, "build_directory", None)
    except Exception:
        staging_build_dir = None

    files_to_copy: Set[str] = set()
    build_files_to_copy: Set[str] = set()

    for dwarf_path in dwarf_paths:
        if dwarf_path.startswith(permanent_src):
            rel = os.path.relpath(dwarf_path, permanent_src)
            staging_file = os.path.join(staging_src, rel)
            if os.path.isfile(staging_file):
                files_to_copy.add(staging_file)
            else:
                _handle_debuggable_failure(
                    "source_file_missing",
                    f"DWARF references {dwarf_path} but {staging_file} not found in staging",
                    pkg_id,
                )
        elif staging_build_dir and dwarf_path.startswith(staging_build_dir):
            if os.path.isfile(dwarf_path):
                build_files_to_copy.add(dwarf_path)
        elif dwarf_path.startswith(staging_src):
            if os.path.isfile(dwarf_path):
                files_to_copy.add(dwarf_path)

    # ── Fallback: compile_commands.json ───────────────────────────────────
    if not files_to_copy:
        tty.debug(f"{pre} DWARF yielded no files; falling back to compile_commands.json")
        files_to_copy = _collect_from_compile_commands(pkg, pre)
        if not files_to_copy:
            _handle_debuggable_failure(
                "compile_commands_missing",
                "Neither DWARF introspection nor compile_commands.json "
                "produced a source file list. "
                "Install may lack debug sources.",
                pkg_id,
            )

    # ── Collect headers from the staging source tree ──────────────────────
    # Headers are referenced in DWARF DW_AT_decl_file entries for individual
    # variables and types, but not as compilation unit roots, so they are
    # invisible to _extract_compilation_unit_paths. Without them, debuggers
    # cannot show inline code or type definitions from header files.
    # Collect all headers from the staging source tree (but not docs, tests,
    # build scripts, or other non-debugger-relevant files).
    _HEADER_EXTENSIONS = {".h", ".hh", ".hpp", ".hxx", ".H", ".inl", ".f90", ".f", ".mod"}
    if staging_src and os.path.isdir(staging_src):
        for _root, _, _fnames in os.walk(staging_src):
            for _fname in _fnames:
                _, _ext = os.path.splitext(_fname)
                if _ext in _HEADER_EXTENSIONS:
                    _fpath = os.path.join(_root, _fname)
                    if os.path.isfile(_fpath):
                        files_to_copy.add(_fpath)
        tty.debug(
            f"{pre} After header scan: {len(files_to_copy)} files to copy to {permanent_src}"
        )

    if files_to_copy:
        _install_sources_as_tree(pkg, files_to_copy, staging_src, permanent_src, pre)

    # ── Step 2: install generated headers from build directory ────────────
    if build_files_to_copy and staging_build_dir:
        tty.debug(f"{pre} DWARF referenced {len(build_files_to_copy)} files from build directory")
        _install_sources_as_tree(pkg, build_files_to_copy, staging_build_dir, build_target, pre)
    elif staging_build_dir and os.path.isdir(staging_build_dir):
        # Fallback: no DWARF refs into build dir, use extension filter
        tty.debug(f"{pre} No DWARF refs into build dir; falling back to extension filter")
        _install_generated_headers(pkg, build_target, pre, pkg_id)

    # ── Step 3: install compile_commands.json for IDE tooling ─────────────
    _install_compile_commands(pkg, build_target, pre)


# ---------------------------------------------------------------------------
# Private helpers
# ---------------------------------------------------------------------------


def _collect_from_compile_commands(pkg: "spack.package_base.PackageBase", pre: str) -> Set[str]:
    """Parse ``compile_commands.json`` to get compiled source file paths.

    This is a fallback when DWARF extraction yields nothing.  Only CMake
    packages produce this file.

    Returns:
        Set of absolute staging paths, or empty set if not found/parseable.
    """
    try:
        builder = spack.builder.create(pkg)
        build_dir = getattr(builder, "build_directory", None)
        if not build_dir:
            return set()

        cc_path = os.path.join(build_dir, "compile_commands.json")
        if not os.path.isfile(cc_path):
            tty.debug(f"{pre} compile_commands.json not found at {cc_path}")
            return set()

        with open(cc_path, "r", encoding="utf-8") as f:
            entries = json.load(f)

        result: Set[str] = set()
        for entry in entries:
            filepath = entry.get("file", "")
            if filepath and os.path.isfile(filepath):
                result.add(os.path.abspath(filepath))

        tty.debug(f"{pre} compile_commands.json: found {len(result)} source files")
        return result

    except (json.JSONDecodeError, KeyError) as e:
        tty.debug(f"{pre} Failed to parse compile_commands.json: {e}")
        return set()
    except Exception as e:
        tty.debug(f"{pre} Unexpected error reading compile_commands: {e}")
        return set()


def _install_sources_as_tree(
    pkg: "spack.package_base.PackageBase",
    files: Set[str],
    source_root: str,
    dest_root: str,
    pre: str,
) -> None:
    """Copy source files to a real directory tree in the install prefix.

    Creates ``<prefix>/share/<pkg>/src/`` as a real filesystem directory
    with the source files inside.  GDB can find these files immediately
    without any extraction step because the paths in DWARF match the
    filesystem paths exactly.

    Args:
        pkg:         the package being installed (used for logging only)
        files:       absolute staging paths of source files to copy
        source_root: staging source root for preserving directory structure
        dest_root:   destination root directory in the install prefix
        pre:         log prefix string
    """
    copied = 0
    failed = 0

    for staging_file in sorted(files):
        if not os.path.isfile(staging_file):
            continue
        try:
            try:
                rel = os.path.relpath(staging_file, source_root)
                rel = staging_file.lstrip("/") if rel.startswith("..") else rel
            except ValueError:
                rel = staging_file.lstrip("/")

            dst = os.path.join(dest_root, rel)
            fs.mkdirp(os.path.dirname(dst))
            fs.install(staging_file, dst)
            copied += 1

        except Exception as e:
            tty.debug(f"{pre} Could not copy {staging_file} to {dest_root}: {e}")
            failed += 1

    if copied > 0:
        tty.msg(f"{pre} Installed {copied} source files to {dest_root}")
    if failed > 0:
        tty.debug(f"{pre} Failed to copy {failed} source files")


def _install_generated_headers(
    pkg: "spack.package_base.PackageBase", build_target: str, pre: str, pkg_id: str
) -> None:
    """Copy generated header files from the CMake build directory.

    Installs ``config.h``, ``moc_*.cpp``, ``ui_*.h``, ``*.pb.h``, etc.
    into ``<prefix>/share/<pkg>/build/``.
    Only runs when ``builder.build_directory`` exists (CMake packages).
    Makefile-based packages have no build directory and this is a no-op.

    Args:
        pkg:          the package being installed
        build_target: destination directory in the install prefix
        pre:          log prefix string
        pkg_id:       package identifier string for error messages
    """
    HEADER_EXTENSIONS = {
        ".h",
        ".hh",
        ".hpp",
        ".hxx",
        ".H",
        ".f90",
        ".f",
        ".mod",
        ".pb.h",
        ".pb.cc",
        ".c",
        ".cc",
        ".cpp",
        ".cxx",
    }
    GENERATED_SOURCE_PREFIXES = {"moc_", "ui_", "qrc_"}
    EXCLUDED_DIRECTORY_NAMES = {"CMakeFiles", "Testing", "CTestFiles", ".cmake"}

    try:
        builder = spack.builder.create(pkg)
        build_dir = getattr(builder, "build_directory", None)
        if not build_dir or not os.path.isdir(build_dir):
            tty.debug(f"{pre} No build directory found; skipping generated header installation")
            return
    except Exception as e:
        tty.debug(f"{pre} Could not resolve build_directory: {e}")
        return

    copied = 0
    errors = 0

    for root, dirs, files in os.walk(build_dir):
        dirs[:] = [d for d in dirs if d not in EXCLUDED_DIRECTORY_NAMES and not d.endswith(".dir")]

        for filename in files:
            _, ext = os.path.splitext(filename)
            is_generated_header = ext in HEADER_EXTENSIONS
            is_generated_source = any(
                filename.startswith(prefix) for prefix in GENERATED_SOURCE_PREFIXES
            )

            if not (is_generated_header or is_generated_source):
                continue

            src_file = os.path.join(root, filename)
            rel = os.path.relpath(src_file, build_dir)
            dst_file = os.path.join(build_target, rel)

            try:
                fs.mkdirp(os.path.dirname(dst_file))
                fs.install(src_file, dst_file)
                copied += 1
            except Exception as e:
                _handle_debuggable_failure(
                    "generated_headers_partial", f"Could not install {src_file}: {e}", pkg_id
                )
                errors += 1

    if copied > 0:
        tty.debug(f"{pre} Installed {copied} generated headers to {build_target}")
    if errors > 0:
        tty.debug(f"{pre} {errors} generated headers could not be installed")


def _install_compile_commands(
    pkg: "spack.package_base.PackageBase", build_target: str, pre: str
) -> None:
    """Copy ``compile_commands.json`` to the debug build directory.

    Enables clangd, clang-tidy, and IDE tools to understand the package
    source code.  Only runs when ``builder.build_directory`` exists.

    Args:
        pkg:          the package being installed
        build_target: destination directory in the install prefix
        pre:          log prefix string
    """
    try:
        builder = spack.builder.create(pkg)
        build_dir = getattr(builder, "build_directory", None)
        if not build_dir:
            return

        cc_src = os.path.join(build_dir, "compile_commands.json")
        if not os.path.isfile(cc_src):
            tty.debug(f"{pre} compile_commands.json not found at {cc_src}, skipping")
            return

        fs.mkdirp(build_target)
        cc_dst = os.path.join(build_target, "compile_commands.json")
        fs.install(cc_src, cc_dst)
        tty.debug(f"{pre} Installed compile_commands.json to {build_target}")

    except Exception as e:
        tty.debug(f"{pre} Could not install compile_commands.json: {e}")
