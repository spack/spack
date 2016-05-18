##############################################################################
# Copyright (c) 2013-2016, Lawrence Livermore National Security, LLC.
# Produced at the Lawrence Livermore National Laboratory.
#
# This file is part of Spack.
# Created by Todd Gamblin, tgamblin@llnl.gov, All rights reserved.
# LLNL-CODE-647188
#
# For details, see https://github.com/llnl/spack
# Please also see the LICENSE file for our notice and the LGPL.
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License (as
# published by the Free Software Foundation) version 2.1, February 1999.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the IMPLIED WARRANTY OF
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the terms and
# conditions of the GNU Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public
# License along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA 02111-1307 USA
##############################################################################
import os
from collections import namedtuple
import imp
import platform as py_platform
import inspect

from llnl.util.lang import memoized, list_modules, key_ordering
from llnl.util.filesystem import join_path
import llnl.util.tty as tty

import spack
import spack.compilers
from spack.util.naming import mod_to_class
from spack.util.environment import get_path
from spack.util.multiproc import parmap
import spack.error as serr


class InvalidSysTypeError(serr.SpackError):
    def __init__(self, sys_type):
        super(InvalidSysTypeError, self).__init__(
            "Invalid sys_type value for Spack: " + sys_type)


class NoSysTypeError(serr.SpackError):
    def __init__(self):
        super(NoSysTypeError, self).__init__(
            "Could not determine sys_type for this machine.")


@key_ordering
class Target(object):
    """ Target is the processor of the host machine.
        The host machine may have different front-end and back-end targets,
        especially if it is a Cray machine. The target will have a name and
        also the module_name (e.g craype-compiler). Targets will also
        recognize which platform they came from using the set_platform method.
        Targets will have compiler finding strategies
    """

    def __init__(self, name, module_name=None):
        self.name = name  # case of cray "ivybridge" but if it's x86_64
        self.module_name = module_name  # craype-ivybridge

    # Sets only the platform name to avoid recursiveness

    def _cmp_key(self):
        return (self.name, self.module_name)

    def __repr__(self):
        return self.__str__()

    def __str__(self):
        return self.name

    def to_dict(self):
        d = {}
        d['name'] = self.name
        d['module_name'] = self.module_name

        return d

@key_ordering
class Platform(object):
    """ Abstract class that each type of Platform will subclass.
        Will return a instance of it once it
        is returned
    """

    priority        = None  # Subclass needs to set this number. This controls order in which platform is detected.
    front_end       = None
    back_end        = None
    default         = None  # The default back end target. On cray ivybridge

    front_os        = None
    back_os         = None
    default_os      = None

    def __init__(self, name):
        self.targets = {}
        self.operating_sys = {}
        self.name = name

    def add_target(self, name, target):
        """Used by the platform specific subclass to list available targets.
        Raises an error if the platform specifies a name
        that is reserved by spack as an alias.
        """
        if name in ['front_end', 'fe', 'back_end', 'be', 'default']:
            raise ValueError(
                "%s is a spack reserved alias "
                "and cannot be the name of a target" % name)
        self.targets[name] = target

    def target(self, name):
        """This is a getter method for the target dictionary
        that handles defaulting based on the values provided by default,
        front-end, and back-end. This can be overwritten
        by a subclass for which we want to provide further aliasing options.
        """
        if name == 'default_target':
            name = self.default
        elif name == 'frontend' or name == 'fe':
            name = self.front_end
        elif name == 'backend' or name == 'be':
            name = self.back_end

        return self.targets.get(name, None)

    def add_operating_system(self, name, os_class):
        """ Add the operating_system class object into the
            platform.operating_sys dictionary
        """
        self.operating_sys[name] = os_class

    def operating_system(self, name):
        if name == 'default_os':
            name = self.default_os
        if name == 'frontend' or name == "fe":
            name = self.front_os
        if name == 'backend' or name == 'be':
            name = self.back_os

        return self.operating_sys.get(name, None)

    
    @classmethod
    def detect(self):
        """ Subclass is responsible for implementing this method.
            Returns True if the Platform class detects that
            it is the current platform
            and False if it's not.
        """
        raise NotImplementedError()

    def __repr__(self):
        return self.__str__()

    def __str__(self):
        return self.name

    def _cmp_key(self):
        return (self.name, (_cmp_key(t) for t in self.targets.values()),
                (_cmp_key(o) for o in self.operating_sys.values()))

@key_ordering
class OperatingSystem(object):
    """ Operating System will be like a class similar to platform extended
        by subclasses for the specifics. Operating System will contain the
        compiler finding logic. Instead of calling two separate methods to
        find compilers we call find_compilers method for each operating system
    """

    def __init__(self, name, version):
        self.name = name
        self.version = version

    def __str__(self):
        return self.name + self.version

    def __repr__(self):
        return self.__str__()

    def _cmp_key(self):
        return (self.name, self.version)


    def find_compilers(self, *paths):
        """
        Return a list of compilers found in the suppied paths.
        This invokes the find() method for each Compiler class,
        and appends the compilers detected to a list.
        """
        if not paths:
            paths = get_path('PATH')
        # Make sure path elements exist, and include /bin directories
        # under prefixes.
        filtered_path = []
        for p in paths:
            # Eliminate symlinks and just take the real directories.
            p = os.path.realpath(p)
            if not os.path.isdir(p):
                continue
            filtered_path.append(p)

            # Check for a bin directory, add it if it exists
            bin = join_path(p, 'bin')
            if os.path.isdir(bin):
                filtered_path.append(os.path.realpath(bin))

        # Once the paths are cleaned up, do a search for each type of
        # compiler.  We can spawn a bunch of parallel searches to reduce
        # the overhead of spelunking all these directories.
        types = spack.compilers.all_compiler_types()
        compiler_lists = parmap(lambda cmp_cls: self.find_compiler(cmp_cls, *filtered_path), types)

        # ensure all the version calls we made are cached in the parent
        # process, as well.  This speeds up Spack a lot.
        clist = reduce(lambda x,y: x+y, compiler_lists)
        return clist

    def find_compiler(self, cmp_cls, *path):
        """Try to find the given type of compiler in the user's
           environment. For each set of compilers found, this returns
           compiler objects with the cc, cxx, f77, fc paths and the
           version filled in.

           This will search for compilers with the names in cc_names,
           cxx_names, etc. and it will group them if they have common
           prefixes, suffixes, and versions.  e.g., gcc-mp-4.7 would
           be grouped with g++-mp-4.7 and gfortran-mp-4.7.
        """
        dicts = parmap(
            lambda t: cmp_cls._find_matches_in_path(*t),
            [(cmp_cls.cc_names,  cmp_cls.cc_version)  + tuple(path),
             (cmp_cls.cxx_names, cmp_cls.cxx_version) + tuple(path),
             (cmp_cls.f77_names, cmp_cls.f77_version) + tuple(path),
             (cmp_cls.fc_names,  cmp_cls.fc_version)  + tuple(path)])

        all_keys = set()
        for d in dicts:
            all_keys.update(d)

        compilers = {}
        for k in all_keys:
            ver, pre, suf = k

            # Skip compilers with unknown version.
            if ver == 'unknown':
                continue

            paths = tuple(pn[k] if k in pn else None for pn in dicts)
            spec = spack.spec.CompilerSpec(cmp_cls.name, ver)

            if ver in compilers:
                prev = compilers[ver]

                # prefer the one with more compilers.
                prev_paths = [prev.cc, prev.cxx, prev.f77, prev.fc]
                newcount  = len([p for p in paths      if p is not None])
                prevcount = len([p for p in prev_paths if p is not None])

                # Don't add if it's not an improvement over prev compiler.
                if newcount <= prevcount:
                    continue

            compilers[ver] = cmp_cls(spec, self, paths)

        return list(compilers.values())

    def to_dict(self):
        d = {}
        d['name'] = self.name
        d['version'] = self.version

        return d

#NOTE: Key error caused because Architecture has no comparison method
@key_ordering
class Arch(object):
    "Architecture is now a class to help with setting attributes"

    def __init__(self, platform_os=None, target=None):
        self.platform = sys_type()
        if platform_os:
            platform_os = self.platform.operating_system(platform_os)
        self.platform_os = platform_os
        if target:
            target = self.platform.target(target)
        self.target = target


    @property
    def concrete(self):
        return all( (self.platform is not None, isinstance(self.platform, Platform),
                     self.platform_os is not None, isinstance(self.platform_os, OperatingSystem),
                     self.target is not None, isinstance(self.target, Target) ) )


    def __str__(self):
        if self.platform.name == 'darwin':
            os_name = self.platform_os.name
        else:
            os_name = str(self.platform_os)

        return (str(self.platform) +"-"+
                os_name + "-" + str(self.target))

    def _cmp_key(self):
        platform = self.platform.name
        os = self.platform_os.name if isinstance(self.platform_os, OperatingSystem) else self.platform_os
        target = self.target.name if isinstance(self.target, Target) else self.target
        return (platform, os, target)

    def to_dict(self):
        d = {}
        platform = self.platform
        platform_os = self.platform_os
        target = self.target

        d['platform'] = self.platform.name
        d['platform_os'] = self.platform_os.to_dict()
        d['target'] = self.target.to_dict()

        return d


def _target_from_dict(target_dict):
    """ Creates new instance of target and assigns all the attributes of
        that target from the dictionary
    """
    target = Target.__new__(Target)
    target.name = target_dict['name']
    target.module_name = target_dict['module_name']
    if 'platform_name' in target_dict:
        target.platform_name = target_dict['platform_name']
    return target

def _operating_system_from_dict(os_dict):
    """ uses platform's operating system method to grab the constructed
        operating systems that are valid on the platform.
    """
# NOTE: Might need a better way to create operating system objects
    operating_system = OperatingSystem.__new__(OperatingSystem)
    operating_system.name = os_dict['name']
    operating_system.version = os_dict['version']
    return operating_system

def arch_from_dict(d):
    """ Uses _platform_from_dict, _operating_system_from_dict, _target_from_dict
        helper methods to recreate the arch tuple from the dictionary read from
        a yaml file
    """
    arch = Arch()

    if d is None:
        return None
    os_dict = d['platform_os']
    target_dict = d['target']

    target = _target_from_dict(target_dict)
    platform_os = _operating_system_from_dict(os_dict)
    arch.target = target
    arch.platform_os = platform_os

    return arch

@memoized
def all_platforms():
    modules = []

    mod_path = spack.platform_path
    mod_string = "spack.platformss"

    for name in list_modules(mod_path):
        mod_name = mod_string + name
        path = join_path(mod_path, name) + ".py"
        mod = imp.load_source(mod_name, path)
        class_name = mod_to_class(name)
        if not hasattr(mod, class_name):
            tty.die('No class %s defined in %s' % (class_name, mod_name))
        cls = getattr(mod, class_name)
        if not inspect.isclass(cls):
            tty.die('%s.%s is not a class' % (mod_name, class_name))

        modules.append(cls)

    return modules

@memoized
def sys_type():
    """ Gather a list of all available subclasses of platforms.
        Sorts the list according to their priority looking. Priority is
        an arbitrarily set number. Detects platform either using uname or
        a file path (/opt/cray...)
    """
    # Try to create a Platform object using the config file FIRST
    platform_list = all_platforms()
    platform_list.sort(key=lambda a: a.priority)

    for platform in platform_list:
        if platform.detect():
            return platform()
