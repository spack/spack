# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
# ----------------------------------------------------------------------------

from spack import *
import os


class GaussianView(Package):
    """GaussView 6 is the latest iteration of a graphical interface used with
    Gaussian. It aids in the creation of Gaussian input files, enables the
    user to run Gaussian calculations from a graphical interface without the
    need for using a command line instruction, and helps in the interpretation
    of Gaussian output"""

    homepage = "https://gaussian.com/gaussview6/"
    manual_download = True

    version('6016',
            '5dd6a8df8c81763e43a308b3a18d2d3b825d3597e9628dcf43e563d1867b9638',
            extension='tbz')

    depends_on('gaussian@16-B.01', type='run')

    def url_for_version(self, version):
        return "file://{0}/gv-{1}-Linux-x86_64.tbz".format(os.getcwd(),
                                                           version)

    def install(self, spec, prefix):
        install_tree(os.getcwd(), self.prefix)

    def setup_run_environment(self, env):
        env.set('GV_DIR', self.prefix)
        env.prepend_path('PATH', self.prefix)
        env.set('GV_LIB_PATH', self.prefix.lib)
        env.prepend_path('GV_LIB_PATH', self.prefix.lib.MesaGL)
        env.prepend_path('LD_LIBRARY_PATH', self.prefix.lib.MesaGL)
        env.set('ALLOWINDIRECT', '1')
        env.prepend_path('QT_PLUGIN_PATH', self.prefix.plugins)
