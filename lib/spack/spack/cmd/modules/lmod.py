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
import functools
import os

import llnl.util.filesystem
import spack.cmd.common.arguments
import spack.cmd.modules


def add_command(parser, command_dict):
    lmod_parser = parser.add_parser(
        'lmod', help='manipulate hierarchical module files'
    )
    sp = spack.cmd.modules.setup_parser(lmod_parser)

    # Set default module file for a package
    setdefault_parser = sp.add_parser(
        'setdefault', help='set the default module file for a package'
    )
    spack.cmd.common.arguments.add_common_arguments(
        setdefault_parser, ['constraint']
    )

    callbacks = dict(spack.cmd.modules.callbacks.items())
    callbacks['setdefault'] = setdefault

    command_dict['lmod'] = functools.partial(
        spack.cmd.modules.modules_cmd, module_type='lmod', callbacks=callbacks
    )


def setdefault(module_type, specs, args):
    """Set the default module file, when multiple are present"""
    # For details on the underlying mechanism see:
    #
    # https://lmod.readthedocs.io/en/latest/060_locating.html#marking-a-version-as-default
    #
    spack.cmd.modules.one_spec_or_raise(specs)
    writer = spack.modules.module_types['lmod'](specs[0])

    module_folder = os.path.dirname(writer.layout.filename)
    module_basename = os.path.basename(writer.layout.filename)
    with llnl.util.filesystem.working_dir(module_folder):
        if os.path.exists('default') and os.path.islink('default'):
            os.remove('default')
        os.symlink(module_basename, 'default')
