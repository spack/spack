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
"""Defines paths that are part of Spack's directory structure.

Do not import other ``spack`` modules here. This module is used
throughout Spack and should bring in a minimal number of external
dependencies.
"""
import os
from llnl.util.filesystem import ancestor


#: This file lives in $prefix/lib/spack/spack/__file__
prefix = ancestor(__file__, 4)

#: synonym for prefix
spack_root = prefix

#: bin directory in the spack prefix
bin_path = os.path.join(prefix, "bin")

#: The spack script itself
spack_script = os.path.join(bin_path, "spack")

# spack directory hierarchy
lib_path              = os.path.join(prefix, "lib", "spack")
external_path         = os.path.join(lib_path, "external")
build_env_path        = os.path.join(lib_path, "env")
module_path           = os.path.join(lib_path, "spack")
command_path          = os.path.join(module_path, "cmd")
platform_path         = os.path.join(module_path, 'platforms')
compilers_path        = os.path.join(module_path, "compilers")
build_systems_path    = os.path.join(module_path, 'build_systems')
operating_system_path = os.path.join(module_path, 'operating_systems')
test_path             = os.path.join(module_path, "test")
hooks_path            = os.path.join(module_path, "hooks")
var_path              = os.path.join(prefix, "var", "spack")
stage_path            = os.path.join(var_path, "stage")
repos_path            = os.path.join(var_path, "repos")
share_path            = os.path.join(prefix, "share", "spack")

# Paths to built-in Spack repositories.
packages_path      = os.path.join(repos_path, "builtin")
mock_packages_path = os.path.join(repos_path, "builtin.mock")

#: User configuration location
user_config_path = os.path.expanduser('~/.spack')


opt_path        = os.path.join(prefix, "opt")
etc_path        = os.path.join(prefix, "etc")
system_etc_path = '/etc'

# GPG paths.
gpg_keys_path      = os.path.join(var_path, "gpg")
mock_gpg_data_path = os.path.join(var_path, "gpg.mock", "data")
mock_gpg_keys_path = os.path.join(var_path, "gpg.mock", "keys")
gpg_path           = os.path.join(opt_path, "spack", "gpg")
