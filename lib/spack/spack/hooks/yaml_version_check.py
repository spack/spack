# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

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
            compilers = data.get('compilers')
            if compilers and len(compilers) > 0:
                if (not isinstance(compilers, list) or
                    'operating_system' not in compilers[0]['compiler']):
                    new_file = os.path.join(scope.path, '_old_compilers.yaml')
                    tty.warn('%s in out of date compilers format. '
                             'Moved to %s. Spack automatically generate '
                             'a compilers config file '
                             % (file_name, new_file))
                    os.rename(file_name, new_file)
