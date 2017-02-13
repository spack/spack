##############################################################################
# Copyright (c) 2013-2016, Lawrence Livermore National Security, LLC.
# Produced at the Lawrence Livermore National Laboratory.
#
# This file is part of Spack.
# Created by Todd Gamblin, tgamblin@llnl.gov, All rights reserved.
# LLNL-CODE-647188
#
# For details, see https://github.com/llnl/spack
# Please also see the LICENSE file for our notice and the LGPL.
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
from __future__ import print_function
import spack
import spack.store
import spack.package
import spack.cmd
import spack.cmd.install as install

description = "Create a configuration script and module, but don't build."

setup_parser = install.setup_common_parser


def get_spconfig_fname(package):
    return 'spconfig.py'


def setup(self, args):
    kwargs = install.validate_args(args)

    # Spec from cli
    spec = spack.cmd.parse_specs(
        args.package, concretize=True, allow_multi=False)
    install.show_spec(spec, args)

    with install.setup_logging(spec, args):
        install.top_install(
            spec, setup=set([spec.name]),
            spconfig_fname_fn=get_spconfig_fname,
            **kwargs)
