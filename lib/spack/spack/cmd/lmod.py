##############################################################################
# Copyright (c) 2013-2017, Lawrence Livermore National Security, LLC.
# Produced at the Lawrence Livermore National Laboratory.
#
# This file is part of Spack.
# Created by Todd Gamblin, tgamblin@llnl.gov, All rights reserved.
# LLNL-CODE-647188
#
# For details, see https://github.com/spack/spack
# Please also see the NOTICE and LICENSE files for our notice and the LGPL.
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

import llnl.util.filesystem
import spack.cmd.common.arguments
import spack.cmd.common.modules

description = "manipulate hierarchical module files"
section = "environment"
level = "short"

#: Type of the modules managed by this command
_module_type = 'lmod'


def setup_parser(subparser):
    sp = spack.cmd.common.modules.setup_parser(subparser)

    # Set default module file for a package
    setdefault = sp.add_parser(
        'setdefault', help='set the default module file for a package'
    )
    spack.cmd.common.arguments.add_common_arguments(
        setdefault, ['constraint']
    )


def setdefault(module_type, specs, args):
    """Set the default module file, when multiple are present"""
    # For details on the underlying mechanism see:
    #
    # https://lmod.readthedocs.io/en/latest/060_locating.html#marking-a-version-as-default
    #
    spack.cmd.common.modules.one_spec_or_raise(specs)
    writer = spack.modules.module_types[_module_type](specs[0])

    module_folder = os.path.dirname(writer.layout.filename)
    module_basename = os.path.basename(writer.layout.filename)
    with llnl.util.filesystem.working_dir(module_folder):
        if os.path.exists('default') and os.path.islink('default'):
            os.remove('default')
        os.symlink(module_basename, 'default')


callbacks = dict(spack.cmd.common.modules.callbacks.items())
callbacks['setdefault'] = setdefault


def lmod(parser, args):
    spack.cmd.common.modules.modules_cmd(
        parser, args, module_type=_module_type, callbacks=callbacks
    )
