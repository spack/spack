# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import glob
import itertools
import json
import os
import pathlib
import platform
import re
import subprocess
import sys
from typing import List, Optional, Set, Union

from spack.error import SpackError
from spack.util import tty
from spack.util import windows_registry as winreg
from spack.version import Version

from ._operating_system import OperatingSystem


def windows_version():
    """Windows version as a Version object"""
    # include the build number as this provides important information
    # for low lever packages and components like the SDK and WDK
    # The build number is the version component that would otherwise
    # be the patch version in semantic versioning, i.e. z of x.y.z
    return Version(platform.version())


class WindowsOs(OperatingSystem):
    """This class represents the Windows operating system.  This will be
    auto detected using the python platform.win32_ver() once we have a
    python setup that runs natively.  The Windows platform will be
    represented using the major version operating system number, e.g.
    10.
    """

    def __init__(self):
        plat_ver = windows_version()
        if plat_ver < Version("10"):
            raise SpackError("Spack is not supported on Windows versions older than 10")
        super().__init__("windows{}".format(plat_ver), plat_ver)

    def __str__(self):
        return self.name

    @property
    def vs_install_paths(self):
        vs_install_paths = []
        root = os.environ.get("ProgramFiles(x86)") or os.environ.get("ProgramFiles")
        if root:
            try:
                extra_args = {"encoding": "mbcs", "errors": "strict"}
                paths = subprocess.check_output(  # type: ignore[call-overload] # novermin
                    [
                        os.path.join(root, "Microsoft Visual Studio", "Installer", "vswhere.exe"),
                        "-prerelease",
                        "-requires",
                        "Microsoft.VisualStudio.Component.VC.Tools.x86.x64",
                        "-property",
                        "installationPath",
                        "-products",
                        "*",
                    ],
                    **extra_args,
                ).strip()
                vs_install_paths = paths.split("\n")
            except (subprocess.CalledProcessError, OSError, UnicodeDecodeError):
                pass
        return vs_install_paths

    @property
    def msvc_paths(self):
        return [os.path.join(path, "VC", "Tools", "MSVC") for path in self.vs_install_paths]

    @property
    def oneapi_root(self):
        root = os.environ.get("ONEAPI_ROOT", "") or os.path.join(
            os.environ.get("ProgramFiles(x86)", ""), "Intel", "oneAPI"
        )
        if os.path.exists(root):
            return root

    @property
    def compiler_search_paths(self):
        # First Strategy: Find MSVC directories using vswhere
        _compiler_search_paths = []
        for p in self.msvc_paths:
            _compiler_search_paths.extend(glob.glob(os.path.join(p, "*", "bin", "Hostx64", "x64")))
        oneapi_root = self.oneapi_root
        if oneapi_root:
            _compiler_search_paths.extend(
                glob.glob(os.path.join(oneapi_root, "compiler", "**", "bin"), recursive=True)
            )

        # Second strategy: Find MSVC via the registry
        def try_query_registry(retry=False):
            winreg_report_error = lambda e: tty.debug(
                'Windows registry query on "SOFTWARE\\WOW6432Node\\Microsoft"'
                f"under HKEY_LOCAL_MACHINE: {str(e)}"
            )
            try:
                # Registry interactions are subject to race conditions, etc and can generally
                # be flakey, do this in a catch block to prevent reg issues from interfering
                # with compiler detection
                msft = winreg.WindowsRegistryView(
                    "SOFTWARE\\WOW6432Node\\Microsoft", winreg.HKEY.HKEY_LOCAL_MACHINE
                )
                return msft.find_subkeys(r"VisualStudio_.*", recursive=False)
            except OSError as e:
                # OSErrors propagated into caller by Spack's registry module are expected
                # and indicate a known issue with the registry query
                # i.e. user does not have permissions or the key/value
                # doesn't exist
                winreg_report_error(e)
                return []
            except winreg.InvalidRegistryOperation as e:
                # Other errors raised by the Spack's reg module indicate
                # an unexpected error type, and are handled specifically
                # as the underlying cause is difficult/impossible to determine
                # without manually exploring the registry
                # These errors can also be spurious (race conditions)
                # and may resolve on re-execution of the query
                # or are permanent (specific types of permission issues)
                # but the registry raises the same exception for all types of
                # atypical errors
                if retry:
                    winreg_report_error(e)
                return []

        vs_entries = try_query_registry()
        if not vs_entries:
            # Occasional spurious race conditions can arise when reading the MS reg
            # typically these race conditions resolve immediately and we can safely
            # retry the reg query without waiting
            # Note: Winreg does not support locking
            vs_entries = try_query_registry(retry=True)

        vs_paths = []

        def clean_vs_path(path):
            path = path.split(",")[0].lstrip("@")
            return str((pathlib.Path(path).parent / "..\\..").resolve())

        for entry in vs_entries:
            try:
                val = entry.get_subkey("Capabilities").get_value("ApplicationDescription").value
                vs_paths.append(clean_vs_path(val))
            except FileNotFoundError as e:
                if hasattr(e, "winerror") and e.winerror == 2:
                    pass
                else:
                    raise

        _compiler_search_paths.extend(vs_paths)
        return _compiler_search_paths


def _windows_drive() -> str:
    """Return Windows drive string extracted from the PROGRAMFILES environment variable,
    which is guaranteed to be defined for all logins.
    """
    match = re.match(r"([a-zA-Z]:)", os.environ["PROGRAMFILES"])
    if match is None:
        raise RuntimeError("cannot read the PROGRAMFILES environment variable")
    return match.group(1)


class WindowsKitExternalPaths:
    @staticmethod
    def find_windows_kit_roots() -> List[str]:
        """Return Windows kit root, typically %programfiles%\\Windows Kits\\10|11\\"""
        if sys.platform != "win32":
            return []
        program_files = os.environ["PROGRAMFILES(x86)"]
        kit_base = os.path.join(program_files, "Windows Kits", "**")
        return glob.glob(kit_base)

    @staticmethod
    def find_windows_kit_bin_paths(
        kit_base: Union[Optional[str], Optional[list]] = None,
    ) -> List[str]:
        """Returns Windows kit bin directory per version"""
        kit_base = WindowsKitExternalPaths.find_windows_kit_roots() if not kit_base else kit_base
        assert kit_base, "Unexpectedly empty value for Windows kit base path"
        if isinstance(kit_base, str):
            kit_base = kit_base.split(";")
        kit_paths = []
        for kit in kit_base:
            kit_bin = os.path.join(kit, "bin")
            kit_paths.extend(glob.glob(os.path.join(kit_bin, "[0-9]*", "*\\")))
        return kit_paths

    @staticmethod
    def find_windows_kit_lib_paths(
        kit_base: Union[Optional[str], Optional[list]] = None,
    ) -> List[str]:
        """Returns Windows kit lib directory per version"""
        kit_base = WindowsKitExternalPaths.find_windows_kit_roots() if not kit_base else kit_base
        assert kit_base, "Unexpectedly empty value for Windows kit base path"
        if isinstance(kit_base, str):
            kit_base = kit_base.split(";")
        kit_paths = []
        for kit in kit_base:
            kit_lib = os.path.join(kit, "Lib")
            kit_paths.extend(glob.glob(os.path.join(kit_lib, "[0-9]*", "*", "*\\")))
        return kit_paths

    @staticmethod
    def find_windows_driver_development_kit_paths() -> List[str]:
        """Provides a list of all installation paths
        for the WDK by version and architecture
        """
        wdk_content_root = os.getenv("WDKContentRoot")
        return WindowsKitExternalPaths.find_windows_kit_lib_paths(wdk_content_root)

    @staticmethod
    def find_windows_kit_reg_installed_roots_paths() -> List[str]:
        reg = winreg.WindowsRegistryView(
            "SOFTWARE\\Microsoft\\Windows Kits\\Installed Roots",
            root_key=winreg.HKEY.HKEY_LOCAL_MACHINE,
        )
        if not reg:
            return []
        kit_root_reg = re.compile(r"KitsRoot[0-9]+")
        root_paths = []
        for kit_root in filter(kit_root_reg.match, reg.get_values().keys()):
            root_paths.extend(
                WindowsKitExternalPaths.find_windows_kit_lib_paths(reg.get_value(kit_root).value)
            )
        return root_paths

    @staticmethod
    def find_windows_kit_reg_sdk_paths() -> List[str]:
        sdk_paths = []
        sdk_regex = re.compile(r"v[0-9]+.[0-9]+")
        windows_reg = winreg.WindowsRegistryView(
            "SOFTWARE\\WOW6432Node\\Microsoft\\Microsoft SDKs\\Windows",
            root_key=winreg.HKEY.HKEY_LOCAL_MACHINE,
        )
        for key in filter(sdk_regex.match, [x.name for x in windows_reg.get_subkeys()]):
            reg = windows_reg.get_subkey(key)
            sdk_paths.extend(
                WindowsKitExternalPaths.find_windows_kit_lib_paths(
                    reg.get_value("InstallationFolder").value
                )
            )
        return sdk_paths


class VisualStudioLayout:
    """Discovery of packages installed or managed by the Visual Studio Installer.

    Handles all VS-managed components: CMake, Ninja, LLVM/Clang, Windows SDK,
    and WDK installed either as VS workload components or as standalone VS installs.
    """

    # Release years for which the path heuristics in this class have been verified.
    # Extend this set when a new VS version ships and the layout is confirmed.
    _KNOWN_VS_YEARS: Set[int] = {2017, 2019, 2022, 2026}

    @staticmethod
    def _vswhere_exe() -> str:
        root = os.environ.get("ProgramFiles(x86)") or os.environ.get("ProgramFiles", "")
        return os.path.join(root, "Microsoft Visual Studio", "Installer", "vswhere.exe")

    @staticmethod
    def _run_vswhere(*args: str) -> List[str]:
        """Run vswhere with given arguments; return non-empty output lines or [] on failure."""
        vswhere = VisualStudioLayout._vswhere_exe()
        if not os.path.isfile(vswhere):
            return []
        try:
            raw = subprocess.check_output(
                [vswhere, *args], encoding="mbcs", errors="strict"
            ).strip()
            return [line for line in raw.splitlines() if line.strip()]
        except (subprocess.CalledProcessError, OSError, UnicodeDecodeError):
            return []

    @staticmethod
    def find_vs_install_paths() -> List[str]:
        """Return installation root directories for all VS editions and versions."""
        paths = VisualStudioLayout._run_vswhere(
            "-prerelease", "-products", "*", "-property", "installationPath"
        )
        if paths:
            VisualStudioLayout._warn_if_vs_newer_than_known()
        return paths

    @staticmethod
    def _warn_if_vs_newer_than_known() -> None:
        max_known = max(VisualStudioLayout._KNOWN_VS_YEARS)
        for year_str in VisualStudioLayout._run_vswhere(
            "-prerelease", "-products", "*", "-property", "catalog_productLineVersion"
        ):
            try:
                year = int(year_str)
            except ValueError:
                continue
            if year > max_known:
                tty.warn(
                    f"Visual Studio {year} is newer than the latest version known to "
                    f"VisualStudioLayout ({max_known}). Detected path heuristics may not "
                    "match this release. Update VisualStudioLayout._KNOWN_VS_YEARS after "
                    "verifying the layout."
                )

    @staticmethod
    def find_cmake_paths() -> List[str]:
        """Return CMake bin directories bundled with Visual Studio."""
        return [
            os.path.join(
                path, "Common7", "IDE", "CommonExtensions", "Microsoft", "CMake", "CMake", "bin"
            )
            for path in VisualStudioLayout.find_vs_install_paths()
        ]

    @staticmethod
    def find_ninja_paths() -> List[str]:
        """Return Ninja directories bundled with Visual Studio."""
        return [
            os.path.join(path, "Common7", "IDE", "CommonExtensions", "Microsoft", "CMake", "Ninja")
            for path in VisualStudioLayout.find_vs_install_paths()
        ]

    @staticmethod
    def find_llvm_paths() -> List[str]:
        """Return Clang/LLVM bin directories bundled with Visual Studio.

        VS installs LLVM under VC/Tools/Llvm within each VS instance directory,
        in architecture-specific subdirectories.
        """
        paths = []
        for vs_root in VisualStudioLayout.find_vs_install_paths():
            for arch in ("x64", "ARM64"):
                candidate = os.path.join(vs_root, "VC", "Tools", "Llvm", arch, "bin")
                if os.path.isdir(candidate):
                    paths.append(candidate)
            # Older VS / x86-only layout without an architecture subdirectory
            fallback = os.path.join(vs_root, "VC", "Tools", "Llvm", "bin")
            if os.path.isdir(fallback):
                paths.append(fallback)
        return paths

    @staticmethod
    def find_sdk_bin_paths() -> List[str]:
        """Return Windows SDK bin directories for SDKs managed by the VS Installer.

        VS records which SDK versions it owns in per-instance state.json.  The actual
        SDK files land in the system-wide Windows Kits tree; this method resolves the
        version-specific bin/<ver>/<arch> directories.
        """
        paths = []
        program_files_x86 = os.environ.get("ProgramFiles(x86)", "")
        kit_bin = os.path.join(program_files_x86, "Windows Kits", "10", "bin")
        for vs_root in VisualStudioLayout.find_vs_install_paths():
            for sdk_ver in VisualStudioLayout._sdk_versions_in_instance(vs_root):
                for arch_dir in glob.glob(os.path.join(kit_bin, sdk_ver, "*")):
                    if os.path.isdir(arch_dir):
                        paths.append(arch_dir)
        return paths

    @staticmethod
    def find_sdk_lib_paths() -> List[str]:
        """Return Windows SDK lib directories for SDKs managed by the VS Installer.

        Returns version-specific Lib/<ver>/<api>/<arch> directories for each SDK
        version installed by the VS Installer.
        """
        paths = []
        program_files_x86 = os.environ.get("ProgramFiles(x86)", "")
        kit_lib = os.path.join(program_files_x86, "Windows Kits", "10", "Lib")
        for vs_root in VisualStudioLayout.find_vs_install_paths():
            for sdk_ver in VisualStudioLayout._sdk_versions_in_instance(vs_root):
                for arch_dir in glob.glob(os.path.join(kit_lib, sdk_ver, "*", "*")):
                    if os.path.isdir(arch_dir):
                        paths.append(arch_dir)
        return paths

    @staticmethod
    def find_wdk_paths() -> List[str]:
        """Return WDK lib directories for WDK installed via the VS Installer.

        The kernel-mode (km) subdirectory distinguishes WDK libs from the SDK.
        Falls back to scanning the Windows Kits tree when WDKContentRoot is absent.
        """
        wdk_root = os.environ.get("WDKContentRoot")
        if wdk_root:
            return WindowsKitExternalPaths.find_windows_kit_lib_paths(wdk_root)
        program_files_x86 = os.environ.get("ProgramFiles(x86)", "")
        kit_lib = os.path.join(program_files_x86, "Windows Kits", "10", "Lib")
        return [
            arch_dir
            for arch_dir in glob.glob(os.path.join(kit_lib, "[0-9]*", "km", "*"))
            if os.path.isdir(arch_dir)
        ]

    @staticmethod
    def find_vs_managed_paths() -> List[str]:
        """Return all VS-managed component paths (CMake, Ninja, LLVM bin, SDK bin, SDK lib)."""
        return (
            VisualStudioLayout.find_cmake_paths()
            + VisualStudioLayout.find_ninja_paths()
            + VisualStudioLayout.find_llvm_paths()
            + VisualStudioLayout.find_sdk_bin_paths()
            + VisualStudioLayout.find_sdk_lib_paths()
        )

    @staticmethod
    def _sdk_versions_in_instance(vs_root: str) -> List[str]:
        """Return Windows SDK versions installed in a VS instance.

        Parses the per-instance state.json written by the VS Installer to extract
        version strings for installed SDK packages.
        """
        instances_root = os.path.join(
            os.environ.get("ProgramData", ""),
            "Microsoft",
            "VisualStudio",
            "Packages",
            "_Instances",
        )
        sdk_pkg_re = re.compile(r"Microsoft\.Windows\.(SDK|UniversalCRT)", re.IGNORECASE)
        sdk_ver_re = re.compile(r"^10\.\d+\.\d+\.\d+$")
        versions: List[str] = []
        for instance_dir in glob.glob(os.path.join(instances_root, "*")):
            state_path = os.path.join(instance_dir, "state.json")
            if not os.path.isfile(state_path):
                continue
            try:
                with open(state_path, encoding="utf-8") as fh:
                    state = json.load(fh)
                if state.get("installationPath", "").lower() != vs_root.lower():
                    continue
                for pkg in state.get("packages", []):
                    pkg_id = pkg.get("id", "")
                    pkg_ver = pkg.get("version", "")
                    if sdk_pkg_re.search(pkg_id) and sdk_ver_re.match(pkg_ver):
                        versions.append(pkg_ver)
            except (OSError, ValueError, KeyError):
                pass
        return versions


def find_win32_additional_install_paths() -> List[str]:
    """Not all programs on Windows live on the PATH
    Return a list of other potential install locations.
    """
    import spack.config
    import spack.util.environment

    drive_letter = _windows_drive()
    windows_search_ext = []
    cuda_re = r"CUDA_PATH[a-zA-Z1-9_]*"
    # The list below should be expanded with other
    # common Windows install locations as necessary
    path_ext_keys = ["I_MPI_ONEAPI_ROOT", "MSMPI_BIN", "MLAB_ROOT", "NUGET_PACKAGES"]
    user = os.environ["USERPROFILE"]
    add_path = lambda key: re.search(cuda_re, key) or key in path_ext_keys
    windows_search_ext.extend([os.environ[key] for key in os.environ.keys() if add_path(key)])
    # note windows paths are fine here as this method should only ever be invoked
    # to interact with Windows
    # Add search path for default Chocolatey (https://github.com/chocolatey/choco)
    # install directory
    windows_search_ext.append("%s\\ProgramData\\chocolatey\\bin" % drive_letter)
    # Add search path for NuGet package manager default install location
    windows_search_ext.append(os.path.join(user, ".nuget", "packages"))
    windows_search_ext.extend(
        spack.config.CONFIG.get("config:additional_external_search_paths", default=[])
    )
    windows_search_ext.extend(spack.util.environment.get_path("PATH"))
    return windows_search_ext


def compute_windows_program_path_for_package(pkg) -> List[str]:
    """Given a package, attempts to compute its Windows program files location,
    and returns the list of best guesses.

    Args:
        pkg: package for which Program Files location is to be computed
    """
    if sys.platform != "win32":
        return []
    # note windows paths are fine here as this method should only ever be invoked
    # to interact with Windows
    program_files = "{}\\Program Files{}\\{}"
    drive_letter = _windows_drive()

    return [
        program_files.format(drive_letter, arch, name)
        for arch, name in itertools.product(("", " (x86)"), (pkg.name, pkg.name.capitalize()))
    ]


def compute_windows_user_path_for_package(pkg) -> List[str]:
    """Given a package attempt to compute its user scoped
    install location, return list of potential locations based
    on common heuristics. For more info on Windows user specific
    installs see:
    https://learn.microsoft.com/en-us/dotnet/api/system.environment.specialfolder?view=netframework-4.8
    """
    if sys.platform != "win32":
        return []

    # Current user directory
    user = os.environ["USERPROFILE"]
    app_data = "AppData"
    app_data_locations = ["Local", "Roaming"]
    user_appdata_install_stubs = [os.path.join(app_data, x) for x in app_data_locations]
    return [
        os.path.join(user, app_data, name)
        for app_data, name in list(
            itertools.product(user_appdata_install_stubs, (pkg.name, pkg.name.capitalize()))
        )
    ] + [os.path.join(user, name) for name in (pkg.name, pkg.name.capitalize())]
