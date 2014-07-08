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
"""This package contains modules with hooks for various stages in the
   Spack install process.  You can add modules here and they'll be
   executaed by package at various times during the package lifecycle.

   Each hook is just a function that takes a package as a parameter.
   Hooks are not executed in any particular order.

   Currently the following hooks are supported:

      * post_install()
      * post_uninstall()

   This can be used to implement support for things like module
   systems (e.g. modules, dotkit, etc.) or to add other custom
   features.
"""
import imp
from llnl.util.lang import memoized, list_modules
from llnl.util.filesystem import join_path
import spack

@memoized
def all_hook_modules():
    modules = []
    for name in list_modules(spack.hooks_path):
        path = join_path(spack.hooks_path, name) + ".py"
        modules.append(imp.load_source('spack.hooks', path))
    return modules


class HookRunner(object):
    def __init__(self, hook_name):
        self.hook_name = hook_name

    def __call__(self, pkg):
        for module in all_hook_modules():
            if hasattr(module, self.hook_name):
                hook = getattr(module, self.hook_name)
                if hasattr(hook, '__call__'):
                    hook(pkg)


#
# Define some functions that can be called to fire off hooks.
#
post_install = HookRunner('post_install')
post_uninstall = HookRunner('post_uninstall')
