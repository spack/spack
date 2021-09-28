# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
"""Aggregate the target processor, the operating system and the target
platform into an architecture object.

On a multiple architecture machine, the architecture spec field can be set to
build a package against any target and operating system that is present on the
platform. On Cray platforms or any other architecture that has different front
and back end environments, the operating system will determine the method of
compiler detection.

There are two different types of compiler detection:

    1. Through the $PATH env variable (front-end detection)
    2. Through the module system. (back-end detection)

Depending on which operating system is specified, the compiler will be detected
using one of those methods.

For platforms such as linux and darwin, the operating system is autodetected.

The command line syntax for specifying an architecture is as follows:

    target=<Target name> os=<OperatingSystem name>

If the user wishes to use the defaults, either target or os can be left out of
the command line and Spack will concretize using the default. These defaults
are set in the 'platforms/' directory which contains the different subclasses
for platforms. If the machine has multiple architectures, the user can
also enter frontend, or fe or backend or be. These settings will concretize
to their respective frontend and backend targets and operating systems.

Platforms are an abstract class that are extended by subclasses. If the user
wants to add a new type of platform (such as cray_xe), they can create a
subclass and set all the class attributes such as priority, front_target,
back_target, front_os, back_os. Platforms also contain a priority class
attribute. A lower number signifies higher priority. These numbers are
arbitrarily set and can be changed though often there isn't much need unless a
new platform is added and the user wants that to be detected first.

Targets are created inside the platform subclasses. Most architecture
(like linux, and darwin) will have only one target family (x86_64) but in the case of
Cray machines, there is both a frontend and backend processor. The user can
specify which targets are present on front-end and back-end architecture

Depending on the platform, operating systems are either autodetected or are
set. The user can set the frontend and backend operating setting by the class
attributes front_os and back_os. The operating system as described earlier,
will be responsible for compiler detection.
"""
import contextlib

import archspec.cpu

import llnl.util.lang as lang

import spack.compiler
import spack.compilers
import spack.config
import spack.operating_systems
import spack.platforms
import spack.spec
import spack.target
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


def arch_for_spec(arch_spec):
    """Transforms the given architecture spec into an architecture object."""
    arch_spec = spack.spec.ArchSpec(arch_spec)
    assert arch_spec.concrete

    arch_plat = spack.platforms.by_name(arch_spec.platform)
    if not (arch_plat.operating_system(arch_spec.os) and
            arch_plat.target(arch_spec.target)):
        sys_type = str(default_arch())
        msg = ("Can't recreate arch for spec {0} on current arch {1}; "
               "spec architecture is too different")
        raise ValueError(msg.format(arch_spec, sys_type))

    return Arch(arch_plat, arch_spec.os, arch_spec.target)


@lang.memoized
def _platform():
    return spack.platforms.host()


#: The "real" platform of the host running Spack. This should not be changed
#: by any method and is here as a convenient way to refer to the host platform.
real_platform = _platform

#: The current platform used by Spack. May be swapped by the use_platform
#: context manager.
platform = _platform


@lang.memoized
def default_arch():
    """Default ``Arch`` object for this machine"""
    return Arch(platform(), 'default_os', 'default_target')


@lang.memoized
def compatible_sys_types():
    """Return a list of all the platform-os-target tuples compatible
    with the current host.
    """
    current_host = archspec.cpu.host()
    compatible_targets = [current_host] + current_host.ancestors
    compatible_archs = [
        str(Arch(platform(), 'default_os', target)) for target in compatible_targets
    ]
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
    global platform

    msg = '"{0}" must be an instance of Platform'
    assert isinstance(new_platform, spack.platforms.Platform), msg.format(new_platform)

    original_platform_fn = platform

    try:
        platform = _PickleableCallable(new_platform)

        # Clear configuration and compiler caches
        spack.config.config.clear_caches()
        spack.compilers._cache_config_files = []

        yield new_platform

    finally:
        platform = original_platform_fn

        # Clear configuration and compiler caches
        spack.config.config.clear_caches()
        spack.compilers._cache_config_files = []
