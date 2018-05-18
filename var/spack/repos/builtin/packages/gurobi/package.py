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
from spack import *
import os


class Gurobi(Package):
    """The Gurobi Optimizer was designed from the ground up to be the fastest,
    most powerful solver available for your LP, QP, QCP, and MIP (MILP, MIQP,
    and MIQCP) problems.

    Note: Gurobi is licensed software. You will need to create an account on
    the Gurobi homepage and download Gurobi Optimizer yourself. Spack will
    search your current directory for the download file. Alternatively, add
    this file to a mirror so that Spack can find it. For instructions on how to
    set up a mirror, see http://spack.readthedocs.io/en/latest/mirrors.html

    Please set the path to licence file with the following command (for bash)
    export GRB_LICENSE_FILE=/path/to/gurobi/license/. See section 4 in
    $GUROBI_HOME/docs/quickstart_linux.pdf for more details."""

    homepage = "http://www.gurobi.com/index"

    version('7.5.2', '01f6dbb8d165838cca1664a1a14e4a85')

    # Licensing
    license_required = True
    license_vars     = ['GRB_LICENSE_FILE']
    license_url      = 'http://www.gurobi.com/downloads/download-center'

    def url_for_version(self, version):
        return "file://{0}/gurobi{1}_linux64.tar.gz".format(os.getcwd(), version)

    def setup_environment(self, spack_env, run_env):
        run_env.set('GUROBI_HOME', self.prefix)

    def install(self, spec, prefix):
        install_tree('linux64', prefix)
