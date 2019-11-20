# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class DealiiParameterGui(CMakePackage):
    """A qt based graphical user interface for editing deal.II .prm parameter
    files."""

    homepage = "https://github.com/dealii/parameter_gui"
    git      = "https://github.com/dealii/parameter_gui.git"

    version('develop', branch='master')

    depends_on('qt')

    def setup_environment(self, spack_env, run_env):
        run_env.set('PARAMETER_GUI_DIR', self.prefix)
