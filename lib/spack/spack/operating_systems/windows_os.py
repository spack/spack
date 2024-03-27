# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import glob
import os
import pathlib
import platform
import subprocess
from typing import List

from spack.error import SpackError
from spack.util import lang, tty
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
    def vs_install_paths(self) -> List[str]:
        """Root directories of the Visual Studio installations on this system.

        Two independent sources are consulted, because neither is sufficient on its own:
        ``vswhere.exe``, which is unavailable when the Visual Studio Installer is absent
        or installed somewhere unexpected, and the Windows registry.

        Roots that no longer exist on disk are discarded. Uninstalling Visual Studio
        routinely leaves its registry entries behind, and those stale entries would
        otherwise be reported as usable toolchains.
        """
        paths = self._vswhere_install_paths() + self._registry_install_paths()
        paths = [path for path in paths if os.path.isdir(path)]
        # Whenever both sources are available they report the same installations.
        return list(lang.dedupe(paths, key=lambda p: os.path.normcase(os.path.normpath(p))))

    def _vswhere_install_paths(self) -> List[str]:
        """Visual Studio install roots reported by ``vswhere.exe``."""
        root = os.environ.get("ProgramFiles(x86)") or os.environ.get("ProgramFiles")
        if not root:
            return []

        def get_vs_component_paths(component: str) -> List[str]:
            try:
                extra_args = {"encoding": "mbcs", "errors": "strict"}
                paths = subprocess.check_output(  # type: ignore[call-overload] # novermin
                    [
                        os.path.join(root, "Microsoft Visual Studio", "Installer", "vswhere.exe"),
                        "-prerelease",
                        "-requires",
                        component,
                        "-property",
                        "installationPath",
                        "-products",
                        "*",
                    ],
                    **extra_args,
                )
            except (subprocess.CalledProcessError, OSError, UnicodeDecodeError):
                return []
            # vswhere prints nothing at all when no instance matches, so drop empty lines
            # rather than reporting a single empty (i.e. relative) install root.
            valid_entries = filter(str.strip, paths.splitlines())
            # return nicely cleaned list of valid vs entries
            return [line.strip() for line in valid_entries]

        components = [
            "Microsoft.VisualStudio.Component.VC.Tools.x86.x64",
            "Microsoft.VisualStudio.Component.VC.Tools.ARM",
            "Microsoft.VisualStudio.Component.VC.Tools.ARM64",
        ]
        vs_install_paths = []
        for component in components:
            vs_install_paths.extend(get_vs_component_paths(component))
        return vs_install_paths

    def _registry_install_paths(self) -> List[str]:
        """Visual Studio install roots recorded in the Windows registry.

        Serves as a fallback for hosts on which ``vswhere.exe`` cannot be located.
        """

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

        def clean_vs_path(path):
            """Derive the install root from a devenv.exe reference recorded by Visual
            Studio, which has the form ``@C:\\...\\Common7\\IDE\\devenv.exe,-1234``."""
            path = path.split(",")[0].lstrip("@")
            return str((pathlib.Path(path).parent / "..\\..").resolve())

        vs_paths = []
        for entry in vs_entries:
            try:
                val = entry.get_subkey("Capabilities").get_value("ApplicationDescription").value
                vs_paths.append(clean_vs_path(val))
            except FileNotFoundError as e:
                if hasattr(e, "winerror") and e.winerror == 2:
                    pass
                else:
                    raise
        return vs_paths

    @property
    def msvc_paths(self) -> List[str]:
        return [os.path.join(path, "VC", "Tools", "MSVC") for path in self.vs_install_paths]

    @property
    def oneapi_root(self):
        root = os.environ.get("ONEAPI_ROOT", "") or os.path.join(
            os.environ.get("ProgramFiles(x86)", ""), "Intel", "oneAPI"
        )
        if os.path.exists(root):
            return root

    @property
    def compiler_search_paths(self) -> List[str]:
        """Directories that may contain a compiler Spack can drive on Windows.

        ``vs_install_paths`` reports installation roots; the compilers themselves live
        several levels below one, so the roots are never search paths in their own right.
        """
        _compiler_search_paths = []
        for p in self.msvc_paths:
            _compiler_search_paths.extend(glob.glob(os.path.join(p, "*", "bin", "*", "*")))
        oneapi_root = self.oneapi_root
        if oneapi_root:
            _compiler_search_paths.extend(
                glob.glob(os.path.join(oneapi_root, "compiler", "**", "bin"), recursive=True)
            )
        return _compiler_search_paths
