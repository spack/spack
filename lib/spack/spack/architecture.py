##############################################################################
# Copyright (c) 2013, Lawrence Livermore National Security, LLC.
# Produced at the Lawrence Livermore National Laboratory.
#
# This file is part of Spack.
# Written by Todd Gamblin, tgamblin@llnl.gov, All rights reserved.
# LLNL-CODE-647188
#
# For details, see https://scalability-llnl.github.io/spack
# Please also see the LICENSE file for our notice and the LGPL.
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License (as published by
# the Free Software Foundation) version 2.1 dated February 1999.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the IMPLIED WARRANTY OF
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the terms and
# conditions of the GNU General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with this program; if not, write to the Free Software Foundation,
# Inc., 59 Temple Place, Suite 330, Boston, MA 02111-1307 USA
##############################################################################
from collections import namedtuple
import imp
import platform as py_platform
import inspect

from llnl.util.lang import memoized, list_modules, key_ordering
from llnl.util.filesystem import join_path
import llnl.util.tty as tty

import spack
from spack.util.naming import mod_to_class
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

    def __init__(self, name, compiler_strategy, module_name=None):
        self.name = name  # case of cray "ivybridge" but if it's x86_64
        self.compiler_strategy = compiler_strategy
        self.module_name = module_name  # craype-ivybridge

    # Sets only the platform name to avoid recursiveness
    def set_platform(self, platform):
        self.platform_name = platform.name

    def to_dict(self):
        d = {}
        d['name'] = self.name
        d['compiler_strategy'] = self.compiler_strategy
        d['module_name'] = self.module_name
        if self.platform_name:
            d['platform'] = self.platform_name
        return d

    @staticmethod
    def from_dict(d):
        if d is None:
            return None
        target = Target.__new__(Target)
        target.name = d['name']
        target.compiler_strategy = d['compiler_strategy']
        target.module_name = d['module_name']
        if 'platform' in d:
            target.platform_name = d['platform']
        return target

    def _cmp_key(self):
        return (self.name, self.module_name)

    def __repr__(self):
        return self.__str__()

    def __str__(self):
        if self.platform_name:
            return self.platform_name + '-' + self.name
        return self.name


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
        target.set_platform(self)
        self.targets[name] = target

    def target(self, name):
        """This is a getter method for the target dictionary 
        that handles defaulting based on the values provided by default, 
        front-end, and back-end. This can be overwritten
        by a subclass for which we want to provide further aliasing options.
        """
        if name == 'default':
            name = self.default
        elif name == 'front_end' or name == 'fe':
            name = self.front_end
        elif name == 'back_end' or name == 'be':
            name = self.back_end

        return self.targets[name]

    #def _detect_linux_os(self):
    #    return OperatingSystem(py_platform.dist()[0], py_platform.dist()[1])

    #def _detect_mac_os(self):
    #    mac_releases = {'10.6': "snowleopard", 
    #                    "10.7": "lion",
    #                    "10.8": "mountainlion",
    #                    "10.9": "mavericks",
    #                    "10.10": "yosemite",
    #                    "10.11": "elcapitan"}     
    #    mac_ver = py_platform.mac_ver()[:-2]
    #    try:
    #        os_name = mac_releases[mac_ver]
    #        return OperatingSystem(os_name, mac_ver)
    #    except KeyError:
    #        os_name = "mac_os"
    #        return OperatingSystem(os_name, mac_ver)
    
    def add_operating_system(self, name, os_class):
        """ Add the operating_system class object into the 
            platform.operating_sys dictionary
        """
        self.operating_sys[name] = os_class

    def operating_system(self, name):
        if name == 'default_os':
            name = self.default_os
        if name == 'front_os':
            name = self.front_os
        if name == 'back_os':
            name = self.back_os

        return self.operating_sys[name]

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

    def __init__(self, name, version, compiler_strategy):
        self.name = name
        self.version = version
        self.compiler_strategy = compiler_strategy
    
    def __str__(self):
        return self.name + self.version

    def __repr__(self):
        return self.__str__()
    
    
    def compiler_strategy(self):
        """ Operating Systems will now be in charge of the compiler finding
            strategy. They will each have their own find_compilers method
            which depending on their compiler strategy will find the compilers
            using a specific method (i.e PATH vs MODULES).
        """
        raise NotImplementedError()

    def _cmp_key(self):
        return (self.name, self.version, self.compiler_strategy)


#NOTE: Key error caused because Architecture has no comparison method
@key_ordering
class Arch(namedtuple("Arch", "platform platform_os target")):
    """ namedtuple for Architecture. Will have it's own __str__ method
        to make printing out the tuple easier and also won't make directory
        paths look odd """
    __slots__ = ()

    def __str__(self):
        return (self.platform.name +"-"+ self.platform_os.name + "-" + self.target.name)
        
    def _cmp_key(self):
        return (self.platform.name, self.platform_os.name, self.target.name)


def _helper_to_dict(arch_field_dict, arch_field_name,  *args):
    """ General method to turn each class in architecture into a 
        dictionary. Takes as argument the class dictionary, 
    """
    d = {}
    d[arch_field_name] = {}
    for items in args:
        d[arch_field_name][items] = arch_field_dict[items]
    return d

def to_dict(arch):
    d = {}
    d['architecture'] = {}

    platform = arch.platform.__dict__
    platform_os = arch.platform_os.__dict__
    target = arch.target.__dict__

    platform_dict = _helper_to_dict(platform,'platform','name')
    os_dict = _helper_to_dict(platform_os, 'platform_os', 'name','version',
                                                          'compiler_strategy')
    target_dict = _helper_to_dict(target,'target', 'name', 
                                            'module_name','platform_name')

    d['architecture'].update(platform_dict)
    d['architecture'].update(os_dict)
    d['architecture'].update(target_dict)

    return d

def _platform_from_dict(platform):
    platform_list = all_platforms()
    platform_names = {plat.__name__.lower():plat for plat in platform_list}
    return platform_names[platform['name']]()


def _target_from_dict(target): 
    target = Target.__new__(Target)
    target.name = d['name']
    target.compiler_strategy = d['compiler_strategy']
    target.module_name = d['module_name']
    if 'platform' in d:
        target.platform_name = d['platform']
    return target

def _operating_system_from_dict(os_dict):
    pass

def arch_from_dict(d):
    if d is None:
        return None
    arch = Arch 
    platform_dict = d['platform']
    platform_os_dict = d['platform_os']
    target_dict = d['target']

    platform = _platform_from_dict(platform_dict)
    platform_os = _operating_system_from_dict(platform_os_dict)
    target = _target_from_dict(target_dict)

    arch.platform = platform
    arch.platform_os = platform_os
    arch.target = target

    return arch

@memoized
def all_platforms():
    modules = []
    for name in list_modules(spack.platform_path):
        mod_name = 'spack.platformss' + name
        path = join_path(spack.platform_path, name) + ".py"
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
