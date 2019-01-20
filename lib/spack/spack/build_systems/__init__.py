# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
import sys
import functools
from types import MethodType
from spack.package import InstallPhase


def get_func_from_method(method):
    if sys.version_info >= (3, 0):
        func = attribute.__func__
    else:
        func = attribute.im_func
    return func


def steal_attribute(pkg, attribute, name_changes):
    """
    Attaches attribute to pkg, while maintaining type information.

    Methods are turned to functions and attached via MethodType
    Properties are captured using fget and attached directly
    All others are attached directly.

    This will need to be revisited if/when a build system adds a multimethod
    function.
    """
    if isinstance(attribute, property):
        return property(attribute.fget)
    elif isinstance(attribute, MethodType):
        func = get_func_from_method(attribute)
        new_method = MethodType(func, pkg, pkg.__class__)
        return new_method
    elif isinstance(attribute, InstallPhase):
        phase_name = name_changes.get(attribute.name, attribute.name)
        if not phase_name:
            # This is an InstallPhase object for a removed phase
            # The return value is thrown away as long as it's an InstallPhase
            return InstallPhase('fake')
        name = '_InstallPhase_%s' % phase_name
        pkg_attr = getattr(pkg.__class__, name)
        pkg_attr.run_before.extend(attribute.run_before)
        pkg_attr.run_after.extend(attribute.run_after)
        return pkg_attr
    else:
        return attribute


def make_package_build_system(pkg, build_system, phase_name_changes):
    """
    Attach all necessary properties of build_system to pkg.

    Necessary properties are passed as names. If the property already exists,
    no change is necessary for that attribute. It is up to the package writer
    to ensure the overriding property is of the appropriate type.

    The name_changes dict allows names to change from pkg to build_system.
    """
    for name in build_system.__dict__:
        new_name = phase_name_changes.get(name, name)
        if new_name:
            if not hasattr(pkg, new_name):
                new_attr = steal_attribute(pkg, getattr(build_system, name),
                                           phase_name_changes)
                if isinstance(new_attr, InstallPhase):
                    # InstallPhse attributes update in place
                    pass
                elif isinstance(new_attr, property):
                    setattr(pkg.__class__, new_name, new_attr)
                else:
                    setattr(pkg, new_name, new_attr)
            else:
                # special handling for multimethods that are overidden for some
                # specs but not for default
                cur_attr = getattr(pkg, new_name)
                if isinstance(cur_attr, functools.partial):
                    try:
                        multimethod = pkg.__class__.__dict__[new_name]
                    except:
                        continue
                    new_attr = get_func_from_method(
                        steal_attribute(pkg,
                                        getattr(build_system, name),
                                        phase_name_changes)
                    )
                    if not multimethod.default:
                        multimethod.default = new_attr
                        functools.update_wrapper(multimethod, new_attr)
