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
import platform as py_platform

from llnl.util.lang import memoized

import spack
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

class Architecture(object):
    def __init__(self, *arch_name):
        
        """ Constructor for the architecture class. Should return a dictionary of name (grabbed from uname) and a strategy for 
            searching for that architecture's compiler. The target passed to it should be a dictionary of names and strategies.
        """
        self.arch_dict = {}
        self.arch_name = arch_name

    def add_arch_strategy(self):
        """ Create a dictionary using the tuples of arch_names"""
        for n in self.arch_name:
            if 'cray' in n.lower():
                self.arch_dict[n] = "MODULES"
            elif 'linux' in n.lower() or 'x86_64' in n.lower():
                self.arch_dict[n] = "PATH"
            else:
                self.arch_dict[n] = "" 
    
    def get_arch_dict(self):
        """ Grab the dictionary from the Architecture class, rather than access the internal Architecture attributes """
        return self.arch_dict
    
    def __eq__(self, other):
        if self.arch_dict != {} and other.arch_dict != {}:
            return self.arch_dict == other.arch_dict
        else:
            return self.arch_name == self.arch_name


def get_sys_type_from_spack_globals():
    """Return the SYS_TYPE from spack globals, or None if it isn't set. Front-end"""
    if not hasattr(spack, "sys_type"):
        return None 
    elif hasattr(spack.sys_type, "__call__"):
        return Architecture(spack.sys_type())
    else:
        return Architecture(spack.sys_type)

# This is livermore dependent. Hard coded for livermore
#def get_sys_type_from_environment():
#    """Return $SYS_TYPE or None if it's not defined."""
#    return os.environ.get('SYS_TYPE')


def get_mac_sys_type():
    """Return a Mac OS SYS_TYPE or None if this isn't a mac.
       Front-end config
    """

    mac_ver = py_platform.mac_ver()[0]
    if not mac_ver:
        return None

    return Architecture("macosx_%s_%s" % (Version(mac_ver).up_to(2), py_platform.machine()))


def get_sys_type_from_uname():
    """ Returns a sys_type from the uname argument 
        Front-end config
    """
    return Architecture(os.uname()[0] + " " + os.uname()[-1])


def get_sys_type_from_config_file():
    """ Should read in a sys_type from the config yaml file. This should be the first thing looked at since
        The user can specify that the architecture is a cray-xc40. A template yaml should be created when spack 
        is installed. Similar to .spackconfig
    """
      
    spack_home_dir = os.environ["HOME"] + "/.spack" 
    yaml_file = os.path.join(spack_home_dir, 'architecture.yaml')
    
    try:
        config_dict = yaml.load(open(yaml_file))  # Fix this to have yaml.load()
        arch = config_dict['architecture']
        front = arch['front']
        back = arch['back']
        return Architecture(front,back)
    
    except:
        print "No architecture.yaml config file found"
        return None


@memoized
def sys_type(): # This function is going to give me issues isn't it??
    """Priority of gathering sys-type.
       1. YAML file that the user specifies the name of the architecture. e.g Cray-XC40 or Cray-XC30
       2. UNAME
       3. GLOBALS
       4. MAC OSX
       Yaml should be a priority here because we want the user to be able to specify the type of architecture to use.
       If there is no yaml present then it should move on to the next function and stop immediately once it gets a 
       arch name
    """
    # Try to create an architecture object using the config file FIRST
    functions = [get_sys_type_from_config_file,
                 get_sys_type_from_uname, 
                 get_sys_type_from_spack_globals,
                 get_mac_sys_type]
    
    # TODO: Test for mac OSX system type but I'm sure it will be okay
    for func in functions:
        sys_type = None
        sys_type = func()
        if sys_type:
            break
    
    return sys_type

