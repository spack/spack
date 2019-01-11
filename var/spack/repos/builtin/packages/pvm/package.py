# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

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
