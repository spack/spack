# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

"""
This module contains all the elements that are required to create an
architecture object. These include, the target processor, the operating system,
and the architecture platform (i.e. cray, darwin, linux, etc) classes.

On a multiple architecture machine, the architecture spec field can be set to
build a package against any target and operating system that is present on the
platform. On Cray platforms or any other architecture that has different front
and back end environments, the operating system will determine the method of
compiler
detection.

There are two different types of compiler detection:
    1. Through the $PATH env variable (front-end detection)
    2. Through the tcl module system. (back-end detection)

Depending on which operating system is specified, the compiler will be detected
using one of those methods.

For platforms such as linux and darwin, the operating system is autodetected
and the target is set to be x86_64.

The command line syntax for specifying an architecture is as follows:

    target=<Target name> os=<OperatingSystem name>

If the user wishes to use the defaults, either target or os can be left out of
the command line and Spack will concretize using the default. These defaults
are set in the 'platforms/' directory which contains the different subclasses
for platforms. If the machine has multiple architectures, the user can
also enter front-end, or fe or back-end or be. These settings will concretize
to their respective front-end and back-end targets and operating systems.
Additional platforms can be added by creating a subclass of Platform
and adding it inside the platform directory.

Platforms are an abstract class that are extended by subclasses. If the user
wants to add a new type of platform (such as cray_xe), they can create a
subclass and set all the class attributes such as priority, front_target,
back_target, front_os, back_os. Platforms also contain a priority class
attribute. A lower number signifies higher priority. These numbers are
arbitrarily set and can be changed though often there isn't much need unless a
new platform is added and the user wants that to be detected first.

Targets are created inside the platform subclasses. Most architecture
(like linux, and darwin) will have only one target (x86_64) but in the case of
Cray machines, there is both a frontend and backend processor. The user can
specify which targets are present on front-end and back-end architecture

Depending on the platform, operating systems are either auto-detected or are
set. The user can set the front-end and back-end operating setting by the class
attributes front_os and back_os. The operating system as described earlier,
will be responsible for compiler detection.
"""
import contextlib

import archspec.cpu

import llnl.util.lang as lang
import llnl.util.tty as tty

import spack.compiler
import spack.compilers
import spack.config
import spack.operating_systems
import spack.paths
import spack.platforms
import spack.spec
import spack.target
import spack.util.classes
import spack.util.executable
import spack.util.spack_yaml as syaml
import spack.version


@lang.lazy_lexicographic_ordering
class Arch(object):
    """Architecture is now a class to help with setting attributes.

    TODO: refactor so that we don't need this class.
    """

    def __init__(self, plat=None, os=None, target=None):
        self.platform = plat
        if plat and os:
            os = self.platform.operating_system(os)
        self.os = os
        if plat and target:
            target = self.platform.target(target)
        self.target = target

        # Hooks for parser to use when platform is set after target or os
        self.target_string = None
        self.os_string = None

    @property
    def concrete(self):
        return all(
            (self.platform is not None,
             isinstance(self.platform, spack.platforms.Platform),
             self.os is not None,
             isinstance(self.os, spack.operating_systems.OperatingSystem),
             self.target is not None, isinstance(self.target, spack.target.Target))
        )

    def __str__(self):
        if self.platform or self.os or self.target:
            if self.platform.name == 'darwin':
                os_name = self.os.name if self.os else "None"
            else:
                os_name = str(self.os)

            return (str(self.platform) + "-" +
                    os_name + "-" + str(self.target))
        else:
            return ''

    def __contains__(self, string):
        return string in str(self)

    # TODO: make this unnecessary: don't include an empty arch on *every* spec.
    def __nonzero__(self):
        return (self.platform is not None or
                self.os is not None or
                self.target is not None)
    __bool__ = __nonzero__

    def _cmp_iter(self):
        if isinstance(self.platform, spack.platforms.Platform):
            yield self.platform.name
        else:
            yield self.platform

        if isinstance(self.os, spack.operating_systems.OperatingSystem):
            yield self.os.name
        else:
            yield self.os

        if isinstance(self.target, spack.target.Target):
            yield self.target.microarchitecture
        else:
            yield self.target

    def to_dict(self):
        str_or_none = lambda v: str(v) if v else None
        d = syaml.syaml_dict([
            ('platform', str_or_none(self.platform)),
            ('platform_os', str_or_none(self.os)),
            ('target', self.target.to_dict_or_value())])
        return syaml.syaml_dict([('arch', d)])

    def to_spec(self):
        """Convert this Arch to an anonymous Spec with architecture defined."""
        spec = spack.spec.Spec()
        spec.architecture = spack.spec.ArchSpec(str(self))
        return spec

    @staticmethod
    def from_dict(d):
        spec = spack.spec.ArchSpec.from_dict(d)
        return arch_for_spec(spec)


@lang.memoized
def get_platform(platform_name):
    """Returns a platform object that corresponds to the given name."""
    platform_list = all_platforms()
    for p in platform_list:
        if platform_name.replace("_", "").lower() == p.__name__.lower():
            return p()


def verify_platform(platform_name):
    """ Determines whether or not the platform with the given name is supported
        in Spack.  For more information, see the 'spack.platforms' submodule.
    """
    platform_name = platform_name.replace("_", "").lower()
    platform_names = [p.__name__.lower() for p in all_platforms()]

    if platform_name not in platform_names:
        tty.die("%s is not a supported platform; supported platforms are %s" %
                (platform_name, platform_names))


def arch_for_spec(arch_spec):
    """Transforms the given architecture spec into an architecture object."""
    arch_spec = spack.spec.ArchSpec(arch_spec)
    assert arch_spec.concrete

    arch_plat = get_platform(arch_spec.platform)
    if not (arch_plat.operating_system(arch_spec.os) and
            arch_plat.target(arch_spec.target)):
        raise ValueError(
            "Can't recreate arch for spec %s on current arch %s; "
            "spec architecture is too different" % (arch_spec, sys_type()))

    return Arch(arch_plat, arch_spec.os, arch_spec.target)


def _all_platforms():
    return spack.platforms.platforms


@lang.memoized
def _platform():
    """Detects the platform for this machine.

    Gather a list of all available subclasses of platforms.
    Sorts the list according to their priority looking. Priority is
    an arbitrarily set number. Detects platform either using uname or
    a file path (/opt/cray...)
    """
    # Try to create a Platform object using the config file FIRST
    platform_list = _all_platforms()
    platform_list.sort(key=lambda a: a.priority)

    for platform_cls in platform_list:
        if platform_cls.detect():
            return platform_cls()


#: The "real" platform of the host running Spack. This should not be changed
#: by any method and is here as a convenient way to refer to the host platform.
real_platform = _platform

#: The current platform used by Spack. May be swapped by the use_platform
#: context manager.
platform = _platform

#: The list of all platform classes. May be swapped by the use_platform
#: context manager.
all_platforms = _all_platforms


@lang.memoized
def default_arch():
    """Default ``Arch`` object for this machine.

    See ``sys_type()``.
    """
    return Arch(platform(), 'default_os', 'default_target')


def sys_type():
    """Print out the "default" platform-os-target tuple for this machine.

    On machines with only one target OS/target, prints out the
    platform-os-target for the frontend.  For machines with a frontend
    and a backend, prints the default backend.

    TODO: replace with use of more explicit methods to get *all* the
    backends, as client code should really be aware of cross-compiled
    architectures.

    """
    return str(default_arch())


@lang.memoized
def compatible_sys_types():
    """Returns a list of all the systypes compatible with the current host."""
    compatible_archs = []
    current_host = archspec.cpu.host()
    compatible_targets = [current_host] + current_host.ancestors
    for target in compatible_targets:
        arch = Arch(platform(), 'default_os', target)
        compatible_archs.append(str(arch))
    return compatible_archs


class _PickleableCallable(object):
    """Class used to pickle a callable that may substitute either
    _platform or _all_platforms. Lambda or nested functions are
    not pickleable.
    """
    def __init__(self, return_value):
        self.return_value = return_value

    def __call__(self):
        return self.return_value


@contextlib.contextmanager
def use_platform(new_platform):
    global platform, all_platforms

    msg = '"{0}" must be an instance of Platform'
    assert isinstance(new_platform, spack.platforms.Platform), msg.format(new_platform)

    original_platform_fn, original_all_platforms_fn = platform, all_platforms

    try:
        platform = _PickleableCallable(new_platform)
        all_platforms = _PickleableCallable([type(new_platform)])

        # Clear configuration and compiler caches
        spack.config.config.clear_caches()
        spack.compilers._cache_config_files = []

        yield new_platform

    finally:
        platform, all_platforms = original_platform_fn, original_all_platforms_fn

        # Clear configuration and compiler caches
        spack.config.config.clear_caches()
        spack.compilers._cache_config_files = []
