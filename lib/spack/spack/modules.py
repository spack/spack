##############################################################################
# Copyright (c) 2013, Lawrence Livermore National Security, LLC.
# Produced at the Lawrence Livermore National Laboratory.
#
# This file is part of Spack.
# Written by Todd Gamblin, tgamblin@llnl.gov, All rights reserved.
# LLNL-CODE-647188
#
# For details, see https://github.com/llnl/spack
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
"""This module contains code for creating environment modules, which
can include dotkits, tcl modules, lmod, and others.

The various types of modules are installed by post-install hooks and
removed after an uninstall by post-uninstall hooks.  This class
consolidates the logic for creating an abstract description of the
information that module systems need.  Currently that includes a
number of directories to be appended to paths in the user's environment:

  * /bin directories to be appended to PATH
  * /lib* directories for LD_LIBRARY_PATH
  * /include directories for CPATH
  * /man* and /share/man* directories for MANPATH
  * the package prefix for CMAKE_PREFIX_PATH

This module also includes logic for coming up with unique names for
the module files so that they can be found by the various
shell-support files in $SPACK/share/spack/setup-env.*.

Each hook in hooks/ implements the logic for writing its specific type
of module file.
"""
__all__ = ['EnvModule', 'Dotkit', 'TclModule']

import os
import os.path
import re
import shutil
import textwrap
from glob import glob

import llnl.util.tty as tty
import spack
from spack.environment import *
from llnl.util.filesystem import join_path, mkdirp

# Registry of all types of modules.  Entries created by EnvModule's metaclass
module_types = {}


def print_help():
    """For use by commands to tell user how to activate shell support."""

    tty.msg("This command requires spack's shell integration.",
            "",
            "To initialize spack's shell commands, you must run one of",
            "the commands below.  Choose the right command for your shell.",
            "",
            "For bash and zsh:",
            "    . %s/setup-env.sh" % spack.share_path,
            "",
            "For csh and tcsh:",
            "    setenv SPACK_ROOT %s"    % spack.prefix,
            "    source %s/setup-env.csh" % spack.share_path,
            "")


class PathInspector(object):
    dirname2varname = {
        'bin': ('PATH',),
        'man': ('MANPATH',),
        'lib': ('LIBRARY_PATH', 'LD_LIBRARY_PATH'),
        'lib64': ('LIBRARY_PATH', 'LD_LIBRARY_PATH'),
        'include': ('CPATH',),
        'pkgconfig': ('PKG_CONFIG_PATH',)
    }

    def __call__(self, env, directory, names):
        for name in names:
            variables = PathInspector.dirname2varname.get(name, None)
            if variables is None:
                continue
            absolute_path = join_path(os.path.abspath(directory), name)
            for variable in variables:
                env.prepend_path(variable, absolute_path)


def inspect_path(path):
    env, inspector = EnvironmentModifications(), PathInspector()
    os.path.walk(path, inspector, env)
    return env


class EnvModule(object):
    name = 'env_module'

    class __metaclass__(type):
        def __init__(cls, name, bases, dict):
            type.__init__(cls, name, bases, dict)
            if cls.name != 'env_module':
                module_types[cls.name] = cls

    def __init__(self, spec=None):
        # category in the modules system
        # TODO: come up with smarter category names.
        self.category = "spack"

        # dict pathname -> list of directories to be prepended to in
        # the module file.
        self._paths = None
        self.spec = spec
        self.pkg = spec.package  # Just stored for convenience

        # short description default is just the package + version
        # packages can provide this optional attribute
        self.short_description = spec.format("$_ $@")
        if hasattr(self.pkg, 'short_description'):
            self.short_description = self.pkg.short_description

        # long description is the docstring with reduced whitespace.
        self.long_description = None
        if self.spec.package.__doc__:
            self.long_description = re.sub(r'\s+', ' ', self.spec.package.__doc__)

    @property
    def paths(self):
        if self._paths is None:
            self._paths = {}

            def add_path(path_name, directory):
                path = self._paths.setdefault(path_name, [])
                path.append(directory)

            # Add paths if they exist.
            for var, directory in [
                    ('PATH', self.spec.prefix.bin),
                    ('MANPATH', self.spec.prefix.man),
                    ('MANPATH', self.spec.prefix.share_man),
                    ('LIBRARY_PATH', self.spec.prefix.lib),
                    ('LIBRARY_PATH', self.spec.prefix.lib64),
                    ('LD_LIBRARY_PATH', self.spec.prefix.lib),
                    ('LD_LIBRARY_PATH', self.spec.prefix.lib64),
                    ('CPATH', self.spec.prefix.include),
                    ('PKG_CONFIG_PATH', join_path(self.spec.prefix.lib, 'pkgconfig')),
                    ('PKG_CONFIG_PATH', join_path(self.spec.prefix.lib64, 'pkgconfig'))]:

                if os.path.isdir(directory):
                    add_path(var, directory)

            # Add python path unless it's an actual python installation
            # TODO : is there a better way to do this?
            # FIXME : add PYTHONPATH to every python package
            if self.spec.name != 'python':
                site_packages = glob(join_path(self.spec.prefix.lib, "python*/site-packages"))
                if site_packages:
                    add_path('PYTHONPATH', site_packages[0])

            # FIXME : Same for GEM_PATH
            if self.spec.package.extends(spack.spec.Spec('ruby')):
                add_path('GEM_PATH', self.spec.prefix)

        return self._paths

    def write(self):
        """Write out a module file for this object."""
        module_dir = os.path.dirname(self.file_name)
        if not os.path.exists(module_dir):
            mkdirp(module_dir)

        # If there are no paths, no need for a dotkit.
        if not self.paths:
            return

        # Construct the changes that needs to be done on the environment for
        env = inspect_path(self.spec.prefix)
        # FIXME : move the logic to inspection
        env.prepend_path('CMAKE_PREFIX_PATH', self.spec.prefix)
        # FIXME : decide how to distinguish between calls done in the installation and elsewhere
        env.extend(self.spec.package.environment_modifications(None))
        # site_specific = ...`
        if not env:
            return

        with open(self.file_name, 'w') as f:
            self._write(f, env)

    def _write(self, stream):
        """To be implemented by subclasses."""
        raise NotImplementedError()


    @property
    def file_name(self):
        """Subclasses should implement this to return the name of the file
           where this module lives."""
        raise NotImplementedError()

    @property
    def use_name(self):
        """Subclasses should implement this to return the name the
           module command uses to refer to the package."""
        raise NotImplementedError()

    def remove(self):
        mod_file = self.file_name
        if os.path.exists(mod_file):
            shutil.rmtree(mod_file, ignore_errors=True)


class Dotkit(EnvModule):
    name = 'dotkit'
    path = join_path(spack.share_path, "dotkit")

    @property
    def file_name(self):
        return join_path(Dotkit.path, self.spec.architecture,
                         '%s.dk' % self.use_name)

    @property
    def use_name(self):
      return "%s-%s-%s-%s-%s" % (self.spec.name, self.spec.version,
                                 self.spec.compiler.name,
                                 self.spec.compiler.version, 
                                 self.spec.dag_hash())

    def _write(self, dk_file, env):
        # Category
        if self.category:
            dk_file.write('#c %s\n' % self.category)

        # Short description
        if self.short_description:
            dk_file.write('#d %s\n' % self.short_description)

        # Long description
        if self.long_description:
            for line in textwrap.wrap(self.long_description, 72):
                dk_file.write("#h %s\n" % line)

        # Path alterations
        for var, dirs in self.paths.items():
            for directory in dirs:
                dk_file.write("dk_alter %s %s\n" % (var, directory))

        # Let CMake find this package.
        dk_file.write("dk_alter CMAKE_PREFIX_PATH %s\n" % self.spec.prefix)


class TclModule(EnvModule):
    name = 'tcl'
    path = join_path(spack.share_path, "modules")
    formats = {
        PrependPath: 'prepend-path {0.name} \"{0.path}\"\n',
        SetEnv: 'setenv {0.name} \"{0.value}\"\n'
    }

    @property
    def file_name(self):
        return join_path(TclModule.path, self.spec.architecture, self.use_name)


    @property
    def use_name(self):
      return "%s-%s-%s-%s-%s" % (self.spec.name, self.spec.version,
                                 self.spec.compiler.name,
                                 self.spec.compiler.version, 
                                 self.spec.dag_hash())

    def process_environment_command(self, env):
        for command in env:
            # FIXME : how should we handle errors here?
            yield self.formats[type(command)].format(command)

    def _write(self, module_file, env):
        """
        Writes a TCL module file for this package

        Args:
            module_file: module file stream
            env: list of environment modifications to be written in the module file
        """
        # TCL Modulefile header
        module_file.write('#%Module1.0\n')
        # TODO : category ?
        # Short description
        if self.short_description:
            module_file.write('module-whatis \"%s\"\n\n' % self.short_description)

        # Long description
        if self.long_description:
            module_file.write('proc ModulesHelp { } {\n')
            doc = re.sub(r'"', '\"', self.long_description)
            module_file.write("puts stderr \"%s\"\n" % doc)
            module_file.write('}\n\n')

        # Environment modifications
        for line in self.process_environment_command(env):
            module_file.write(line)

    # FIXME : REMOVE
    # def _write(self, m_file):
    #     # TODO: cateogry?
    #     m_file.write('#%Module1.0\n')
    #
    #     # Short description
    #     if self.short_description:
    #         m_file.write('module-whatis \"%s\"\n\n' % self.short_description)
    #
    #     # Long description
    #     if self.long_description:
    #         m_file.write('proc ModulesHelp { } {\n')
    #         doc = re.sub(r'"', '\"', self.long_description)
    #         m_file.write("puts stderr \"%s\"\n" % doc)
    #         m_file.write('}\n\n')
    #
    #     # Path alterations
    #     for var, dirs in self.paths.items():
    #         for directory in dirs:
    #             m_file.write("prepend-path %s \"%s\"\n" % (var, directory))
    #
    #     m_file.write("prepend-path CMAKE_PREFIX_PATH \"%s\"\n" % self.spec.prefix)
