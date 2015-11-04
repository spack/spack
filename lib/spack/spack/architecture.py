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

from llnl.util.lang import memoized, list_modules
from llnl.util.filesystem import join_path
import llnl.util.tty as tty

import spack
from spack.util.naming import mod_to_class
import spack.error as serr
from spack.version import Version
from external import yaml

class InvalidSysTypeError(serr.SpackError):
    def __init__(self, sys_type):
        super(InvalidSysTypeError, self).__init__("Invalid sys_type value for Spack: " + sys_type)


class NoSysTypeError(serr.SpackError):
    def __init__(self):
        super(NoSysTypeError, self).__init__("Could not determine sys_type for this machine.")


class Target(object):
    """ Target is the processor of the host machine. The host machine may have different front-end
        and back-end targets, especially if it is a Cray machine. The target will have a name and
        also the module_name (e.g craype-compiler). Targets will also recognize which architecture
        they came from using the set_architecture method. Targets will have compiler finding strategies
        """
    default_strategy = None # Can probably add a compiler path here

    def __init__(self,name, module_name=None):
        self.name = name # case of cray "ivybridge" but if it's x86_64
        self.module_name = module_name # craype-ivybridge

    def set_architecture(self, architecture): # Target should get the architecture class.
        self.architecture = architecture
        
    @property
    def compiler_strategy(self):
        if default_strategy:
            return default_strategy
        elif self.module_name: # If there is a module_name given then use MODULES
            return "MODULES"
        else:
            return "PATH"

class Architecture(object):
    """ Abstract class that each type of Architecture will subclass. Will return a instance of it once it 
        is returned
    """

    priority        = None # Subclass needs to set this number. This controls order in which arch is detected.
    front_end       = None
    back_end        = None
    default         = None # The default back end target. On cray ivybridge

    def __init__(self, name):
        self.targets = {}
        self.name = name

    def add_target(self, name, target):
        target.set_architecture(self)
        self.targets[name] = target          
    
    def target(self, name):
        """This is a getter method for the target dictionary that handles defaulting based
        on the values provided by default, front-end, and back-end. This can be overwritten
        by a subclass for which we want to provide further aliasing options.
        """
        if name == 'default':
            name = self.default
        elif name == 'front_end' or name == 'fe':
            name = self.front_end
        elif name == 'back_end' or name == 'be':
            name = self.back_end

        return self.targets[name]

    @classmethod
    def detect(self):
        """ Subclass is responsible for implementing this method. 
            Returns True if the architecture detects if it is the current architecture
            and False if it's not.
        """
        raise NotImplementedError()
    
    def __str__(self):
        return self.name


def get_sys_type_from_spack_globals():
    """Return the SYS_TYPE from spack globals, or None if it isn't set."""
    if not hasattr(spack, "sys_type"):
        return None 
    elif hasattr(spack.sys_type, "__call__"):
        return spack.sys_type() #If in __init__.py there is a sys_type() then call that
    else:
        return spack.sys_type # Else use the attributed which defaults to None


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
    return "macosx_%s_%s" % (Version(mac_ver).up_to(2), py_platform.machine())


def get_sys_type_from_uname():
    """ Returns a sys_type from the uname argument 
        Front-end config
    """
    try:
        arch_proc = subprocess.Popen(['uname', '-i'], stdout = subprocess.PIPE)
        arch, _ = arch_proc.communicate()
        return arch.strip()
    except:
        return None

def get_sys_type_from_config_file():
     
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
def all_architectures():
    modules = []
    for name in list_modules(spack.arch_path):
        mod_name = 'spack.architectures' + name
        path = join_path(spack.arch_path, name) + ".py"
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
    architecture_list = all_architectures() 
    architecture_list.sort(key = lambda a: a.priority) 
    
    for arch in architecture_list:
        if arch.detect():
            return arch()

