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
"""This module contains code for creating environment modules, which
can include dotkits, tcl modules, lmod, and others.

The various types of modules are installed by post-install hooks and
removed after an uninstall by post-uninstall hooks.  This class
consolidates the logic for creating an abstract description of the
information that module systems need.  Currently that includes a
number directories to be appended to paths in the user's environment:

  * /bin directories to be appended to PATH
  * /lib* directories for LD_LIBRARY_PATH
  * /man* and /share/man* directories for LD_LIBRARY_PATH
  * the package prefix for CMAKE_PREFIX_PATH

This module also includes logic for coming up with unique names for
the module files so that they can be found by the various
shell-support files in $SPACK/share/spack/setup-env.*.

Each hook in hooks/ implements the logic for writing its specific type
of module file.
"""
__all__ = ['EnvModule', 'Dotkit', 'TclModule']

import os
import re
import textwrap
import shutil
from contextlib import closing

import llnl.util.tty as tty
from llnl.util.filesystem import join_path, mkdirp

import spack

dotkit_path  = join_path(spack.share_path, "dotkit")
tcl_mod_path = join_path(spack.share_path, "modules")

def print_help():
    """For use by commands to tell user how to activate shell support."""

    tty.msg("Spack module/dotkit support is not initialized.",
            "",
            "To use dotkit or modules with Spack, you must first run",
            "one of the commands below.  You can copy/paste them.",
            "",
            "For bash and zsh:",
            "    . %s/setup-env.sh" % spack.share_path,
            "",
            "For csh and tcsh:",
            "    setenv SPACK_ROOT %s"    % spack.prefix,
            "    source %s/setup-env.csh" % spack.share_path,
            "")


class EnvModule(object):
    def __init__(self, pkg=None):
        # category in the modules system
        # TODO: come up with smarter category names.
        self.category = "spack"

        # Descriptions for the module system's UI
        self.short_description = ""
        self.long_description = ""

        # dict pathname -> list of directories to be prepended to in
        # the module file.
        self._paths = None
        self.pkg = pkg


    @property
    def paths(self):
        if self._paths is None:
            self._paths = {}

            def add_path(self, path_name, directory):
                path = self._paths.setdefault(path_name, [])
                path.append(directory)

            # Add paths if they exist.
            for var, directory in [
                    ('PATH', self.pkg.prefix.bin),
                    ('MANPATH', self.pkg.prefix.man),
                    ('MANPATH', self.pkg.prefix.share_man),
                    ('LD_LIBRARY_PATH', self.pkg.prefix.lib),
                    ('LD_LIBRARY_PATH', self.pkg.prefix.lib64)]:

                if os.path.isdir(directory):
                    add_path(var, directory)

            # short description is just the package + version
            # TODO: maybe packages can optionally provide it.
            self.short_description = self.pkg.spec.format("$_ $@")

            # long description is the docstring with reduced whitespace.
            if self.pkg.__doc__:
                self.long_description = re.sub(r'\s+', ' ', self.pkg.__doc__)

        return self._paths


    def write(self):
        """Write out a module file for this object."""
        module_dir = os.path.dirname(self.file_name)
        if not os.path.exists():
            mkdirp(module_dir)

        # If there are no paths, no need for a dotkit.
        if not self.paths:
            return

        with closing(open(self.file_name)) as f:
            self._write(f)


    def _write(self, stream):
        """To be implemented by subclasses."""
        raise NotImplementedError()


    @property
    def file_name(self):
        """Subclasses should implement this to return the name of the file
           where this module lives."""
        return self.pkg.spec.format('$_$@$%@$+$=$#')


    def remove(self):
        mod_file = self.file_name
        if os.path.exists(mod_file):
            shutil.rmtree(mod_file, ignore_errors=True)


class Dotkit(EnvModule):
    @property
    def file_name(self):
        spec = self.pkg.spec
        return join_path(dotkit_path, spec.architecture,
                         spec.format('$_$@$%@$+$#.dk'))


    def _write(self, dk_file):
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
        dk_file.write("dk_alter CMAKE_PREFIX_PATH %s\n" % pkg.prefix)


class TclModule(EnvModule):
    @property
    def file_name(self):
        spec = self.pkg.spec
        return join_path(tcl_mod_path, spec.architecture,
                         spec.format('$_$@$%@$+$#'))


    def _write(self, m_file):
        # TODO: cateogry?
        m_file.write('#%Module1.0\n')

        # Short description
        if self.short_description:
            m_file.write('module-whatis \"%s\"\n\n' % self.short_description)

        # Long description
        if self.long_description:
            m_file.write('proc ModulesHelp { } {\n')
            doc = re.sub(r'"', '\"', self.long_description)
            m_file.write("puts stderr \"%s\"\n" % doc)
            m_file.write('}\n\n')

        # Path alterations
        for var, dirs in self.paths.items():
            for directory in dirs:
                m_file.write("prepend-path %s \"%s\"\n" % (var, directory))

        m_file.write("prepend-path CMAKE_PREFIX_PATH \"%s\"\n" % pkg.prefix)
