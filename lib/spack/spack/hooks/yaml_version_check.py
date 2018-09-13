##############################################################################
# Copyright (c) 2013-2018, Lawrence Livermore National Security, LLC.
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
"""Yaml Version Check is a module for ensuring that config file
formats are compatible with the current version of Spack."""
import os.path
import os
import llnl.util.tty as tty
import spack.util.spack_yaml as syaml
import spack.config


def pre_run():
    check_compiler_yaml_version()


def check_compiler_yaml_version():
    config = spack.config.config

    for scope in config.file_scopes:
        file_name = os.path.join(scope.path, 'compilers.yaml')
        data = None
        if os.path.isfile(file_name):
            with open(file_name) as f:
                data = syaml.load(f)

        if data:
            compilers = data['compilers']
            if len(compilers) > 0:
                if (not isinstance(compilers, list) or
                    'operating_system' not in compilers[0]['compiler']):
                    new_file = os.path.join(scope.path, '_old_compilers.yaml')
                    tty.warn('%s in out of date compilers format. '
                             'Moved to %s. Spack automatically generate '
                             'a compilers config file '
                             % (file_name, new_file))
                    os.rename(file_name, new_file)
