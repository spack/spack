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
import subprocess


class Pvm(MakefilePackage):
    """PVM (Parallel Virtual Machine) is a software package that permits a
    heterogeneous collection of Unix and/or Windows computers hooked together
    by a network to be used as a single large parallel computer."""

    homepage = "http://www.csm.ornl.gov/pvm/pvm_home.html"
    url      = "http://www.netlib.org/pvm3/pvm3.4.6.tgz"

    version('3.4.6', '7b5f0c80ea50b6b4b10b6128e197747b')

    parallel = False

    @property
    def pvm_arch(self):
        """Returns the appropriate PVM_ARCH."""
        process = subprocess.Popen(['lib/pvmgetarch'], stdout=subprocess.PIPE)
        return process.communicate()[0].strip()

    def edit(self, spec, prefix):
        # Before building PVM, you must set the environment
        # variable "PVM_ROOT" to the path where PVM resides
        env['PVM_ROOT'] = self.stage.source_path

    def install(self, spec, prefix):
        pvm_arch = self.pvm_arch

        install_tree(join_path('bin', pvm_arch), prefix.bin)
        install_tree('include', prefix.include)
        install_tree(join_path('lib', pvm_arch), prefix.lib)
        install_tree('man', prefix.man)

    def setup_environment(self, spack_env, run_env):
        # Before running PVM, you must set the environment
        # variable "PVM_ROOT" to the path where PVM resides
        run_env.set('PVM_ROOT', self.prefix)
