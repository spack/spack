# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import platform as py_platform
import re

from spack.util.executable import Executable
from spack.version import Version

from ._operating_system import OperatingSystem


def macos_version():
    """temporary workaround to return a macOS version as a Version object
    """
    swvers = Executable('sw_vers')
    output = swvers(output=str, fail_on_error=False)
    match = re.search(r'ProductVersion:\s*([0-9.]+)', output)
    if match:
        return Version(match.group(1))

    # Fall back to python-reported version, which can be inaccurate around
    # macOS 11 (e.g. showing 10.16 for macOS 12)
    return Version(py_platform.mac_ver()[0])


def macos_cltools_version():
    """Find the last installed version of the CommandLineTools.

    The CLT version might only affect the build if it's selected as the macOS
    SDK path.
    """
    pkgutil = Executable('pkgutil')
    output = pkgutil('--pkg-info=com.apple.pkg.cltools_executables',
                     output=str, fail_on_error=False)
    match = re.search(r'version:\s*([0-9.]+)', output)
    if match:
        return Version(match.group(1))

    # No CLTools installed by package manager: try Xcode
    output = pkgutil('--pkg-info=com.apple.pkg.Xcode',
                     output=str, fail_on_error=False)
    match = re.search(r'version:\s*([0-9.]+)', output)
    if match:
        return Version(match.group(1))

    return None


def macos_sdk_path():
    """Return path to the active macOS SDK.
    """
    xcrun = Executable('xcrun')
    return xcrun('--show-sdk-path', output=str).rstrip()


def macos_sdk_version():
    """Return the version of the active macOS SDK.

    The SDK version usually corresponds to the installed Xcode version and can
    affect how some packages (especially those that use the GUI) can fail. This
    information should somehow be embedded into the future "compilers are
    dependencies" feature.

    The macOS deployment target cannot be greater than the SDK version, but
    usually it can be at least a few versions less.
    """
    xcrun = Executable('xcrun')
    return Version(xcrun('--show-sdk-version', output=str).rstrip())


class MacOs(OperatingSystem):
    """This class represents the macOS operating system. This will be
    auto detected using the python platform.mac_ver. The macOS
    platform will be represented using the major version operating
    system name, i.e el capitan, yosemite...etc.
    """

    def __init__(self):
        """Autodetects the mac version from a dictionary.

        If the mac version is too old or too new for Spack to recognize,
        will use a generic "macos" version string until Spack is updated.
        """
        mac_releases = {
            '10.0':  'cheetah',
            '10.1':  'puma',
            '10.2':  'jaguar',
            '10.3':  'panther',
            '10.4':  'tiger',
            '10.5':  'leopard',
            '10.6':  'snowleopard',
            '10.7':  'lion',
            '10.8':  'mountainlion',
            '10.9':  'mavericks',
            '10.10': 'yosemite',
            '10.11': 'elcapitan',
            '10.12': 'sierra',
            '10.13': 'highsierra',
            '10.14': 'mojave',
            '10.15': 'catalina',
            '10.16': 'bigsur',
            '11': 'bigsur',
            '12': 'monterey',
        }

        version = macos_version()

        # Big Sur versions go 11.0, 11.0.1, 11.1 (vs. prior versions that
        # only used the minor component)
        part = 1 if version >= Version('11') else 2

        mac_ver = str(version.up_to(part))
        name = mac_releases.get(mac_ver, "macos")
        super(MacOs, self).__init__(name, mac_ver)

    def __str__(self):
        return self.name
