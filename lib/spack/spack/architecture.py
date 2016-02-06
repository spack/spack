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
import os
import imp
import platform as py_platform
import inspect

from llnl.util.lang import memoized, list_modules, key_ordering
from llnl.util.filesystem import join_path
import llnl.util.tty as tty

import spack
from spack.util.naming import mod_to_class
import spack.error as serr
from spack.version import Version
from external import yaml

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
        The host machine may have different front-end
        and back-end targets, especially if it is a Cray machine. 
        The target will have a name and module_name (e.g craype-compiler). 
        Targets will also recognize which platform
        they came from using the set_platform method. 
        Targets will have compiler finding strategies
        """

    def __init__(self, name, compiler_strategy, module_name=None):
        self.name = name # case of cray "ivybridge" but if it's x86_64
        self.compiler_strategy = compiler_strategy
        self.module_name = module_name # craype-ivybridge

    # Sets only the platform name to avoid recursiveness    
    def set_platform(self, platform):
        self.platform_name = platform.name

    def set_operating_system(self, operating_sys):
        self.platform_os = operating_sys

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
        return (self.name, self.compiler_strategy, 
                self.module_name, self.platform_os)

    def __repr__(self):
        return self.__str__()

    def __str__(self):
        if self.platform_name and self.platform_os:
            return (self.platform_name + '-' + 
                    self.platform_os + '-'  + self.name)
        return self.name

@key_ordering
class Platform(object):
    """ Abstract class that each type of Platform will subclass.
        Will return a instance of it once it
        is returned
    """

    priority        = None # Subclass needs to set this number. This controls order in which platform is detected.

    front_end       = None
    back_end        = None
    default         = None # The default back end target. On cray ivybridge
    
    front_os        = None
    back_os         = None
    default_os      = None

    def __init__(self, name):
        self.targets = {}
        self.name = name

    def add_target(self, name, target):
        """Used by the platform specific subclass to list available targets. 
            Raises an error if the platform specifies a name 
            that is reserved by spack as an alias.
        """
        if name in ['front_end', 'fe', 'back_end', 'be', 'default']:
            raise ValueError(
                            "%s is a spack reserved" \
                             "alias and cannot be the name of a target" 
                             % name)

        target.set_operating_system(self.platform_os())
        target.set_platform(self)
        self.targets[name] = target

    def target(self, name):
        """This is a getter method for the target dictionary that 
        handles defaulting based on the values provided by default, 
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
    
    def _detect_linux_os(self):
        """ If it is one a linux machine use the python method platform.dist()
        """
        os_name = py_platform.dist()[0]
        version = py_platform.dist()[1]
 a      return os_name + version

    def _detect_mac_os(self):
        """If it is on a mac machine then use the python method platform.mac_ver
        """
        mac_releases = {'10.6' : 'snowleopard', '10.7' : 'lion',
                        '10.8' : 'mountainlion', '10.9' : 'mavericks',
                        '10.10' : 'yosemite', '10.11' : 'elcapitan'}
        
        mac_ver = py_platform.mac_ver()
        try:
            os_name = mac_releases[mac_ver]
            mac_ver = Version(mac_ver) 
        
        except KeyError:
            os_name = 'mac_os'

        return os_name 
    
    def set_os(self):
        """ Set the OS according to the platform it is on. Darwin and Linux
            will simply be an auto-detected linux distro or mac release. The
            special cases will be for Cray and BGQ machines which have two
            different OS for login and compute nodes. The client should provide
            the name and major version of the operating system
        """
        if self.name == 'darwin':
            self.default_os = self._detect_mac_os()
        else:
            self.default_os = self._detect_linux_os()

    def platform_os(self, name=None):
        """ Get the platform operating system from the platform """
        if name == 'front_os':
            return self.front_os
        elif name == 'back_os':
            return self.back_os
        else:
            return self.default_os

    @classmethod
    def detect(self):
        """ Subclass is responsible for implementing this method.
            Returns True if the Platform class detects that it is the current platform
            and False if it's not.
        """
        raise NotImplementedError()


    def __repr__(self):
        return self.__str__()

    def __str__(self):
        return self.name

    def _cmp_key(self):
        return (self.name, (_cmp_key(t) for t in self.targets.values()))

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
    platform_list.sort(key = lambda a: a.priority)

    for platform in platform_list:
        if platform.detect():
            return platform()

