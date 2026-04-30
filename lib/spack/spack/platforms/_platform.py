# Copyright Spack Project Developers. See COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
import warnings
from typing import Optional

import spack.vendor.archspec.cpu

import spack.llnl.util.lang


@spack.llnl.util.lang.lazy_lexicographic_ordering
class Platform:
    """Platform is an abstract class extended by subclasses.

    Platform also contain a priority class attribute. A lower number signifies higher
    priority. These numbers are arbitrarily set and can be changed though often there
    isn't much need unless a new platform is added and the user wants that to be
    detected first.
    """

    # Subclass sets number. Controls detection order
    priority: Optional[int] = None

    #: binary formats used on this platform; used by relocation logic
    binary_formats = ["elf"]

    default: str
    default_os: str

    reserved_targets = ["default_target", "frontend", "fe", "backend", "be"]
    reserved_oss = ["default_os", "frontend", "fe", "backend", "be"]
    deprecated_names = ["frontend", "fe", "backend", "be"]

    def __init__(self, name):
        self.targets = {}
        self.operating_sys = {}
        self.name = name
        self._init_targets()

    def add_target(self, name: str, target: spack.vendor.archspec.cpu.Microarchitecture) -> None:
        if name in Platform.reserved_targets:
            msg = f"{name} is a spack reserved alias and cannot be the name of a target"
            raise ValueError(msg)
        self.targets[name] = target

    def _init_targets(self):
        self.default = spack.vendor.archspec.cpu.host().name
        for name, microarchitecture in spack.vendor.archspec.cpu.TARGETS.items():
            self.add_target(name, microarchitecture)

    def target(self, name):
        name = str(name)
        if name in Platform.deprecated_names:
            warnings.warn(f"target={name} is deprecated, use target={self.default} instead")

        if name in Platform.reserved_targets:
            name = self.default

        return self.targets.get(name, None)

    def add_operating_system(self, name, os_class):
        if name in Platform.reserved_oss + Platform.deprecated_names:
            msg = f"{name} is a spack reserved alias and cannot be the name of an OS"
            raise ValueError(msg)
        self.operating_sys[name] = os_class

    def default_target(self):
        return self.target(self.default)

    def default_operating_system(self):
        return self.operating_system(self.default_os)

    def operating_system(self, name):
        if name in Platform.deprecated_names:
            warnings.warn(f"os={name} is deprecated, use os={self.default_os} instead")

        if name in Platform.reserved_oss:
            name = self.default_os

        return self.operating_sys.get(name, None)

    def setup_platform_environment(self, pkg, env):
        """Platform-specific build environment modifications.

        This method is meant to be overridden by subclasses, when needed.
        """
        pass

    @classmethod
    def detect(cls):
        """Returns True if the host platform is detected to be the current Platform class,
        False otherwise.

        Derived classes are responsible for implementing this method.
        """
        raise NotImplementedError()

    def __repr__(self):
        return self.__str__()

    def __str__(self):
        return self.name

    def _cmp_iter(self):
        yield self.name
        yield self.default
        yield self.default_os

        def targets():
            for t in sorted(self.targets.values()):
                yield t._cmp_iter

        yield targets

        def oses():
            for o in sorted(self.operating_sys.values()):
                yield o._cmp_iter

        yield oses

    def to_json(self):
        """Serialize platform to JSON-compatible dict."""
        return {
            "name": self.name,
            "default": self.default,
            "default_os": self.default_os,
            "operating_sys": {name: os.to_dict() for name, os in self.operating_sys.items()},
        }

    @classmethod
    def from_json_base(cls, platform_cls, data):
        """Create a platform from JSON data without platform-specific initialization.

        This method bypasses the normal __init__ to avoid platform-specific code that
        may not work on the current host (e.g., instantiating LinuxDistro on macOS).

        Args:
            platform_cls: The platform class to instantiate (e.g., Linux, Darwin)
            data: dict with keys:
                - 'name': platform name (string)
                - 'default': default target name (string)
                - 'default_os': default OS name (string)
                - 'operating_sys': dict mapping OS names to dicts with 'name' and 'version'

        Returns:
            Platform instance populated from the provided data
        """
        from spack.operating_systems import OperatingSystem

        # Create instance without calling __init__
        instance = platform_cls.__new__(platform_cls)

        # Manually initialize base attributes
        instance.name = data["name"]
        instance.default = data["default"]
        instance.default_os = data["default_os"]
        instance.targets = {}
        instance.operating_sys = {}

        # Initialize targets (reusing the normal method but don't auto-detect default)
        for name, microarchitecture in spack.vendor.archspec.cpu.TARGETS.items():
            instance.add_target(name, microarchitecture)

        # Recreate operating systems from JSON data
        for os_name, os_data in data.get("operating_sys", {}).items():
            os_instance = OperatingSystem.from_json(os_data)
            instance.operating_sys[os_name] = os_instance

        return instance
