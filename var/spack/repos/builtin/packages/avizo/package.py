# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *
import os
import tarfile


class Avizo(Package):
    """Avizo is a 3D analysis software for scientific and industrial data.
    Wherever three-dimensional imaging data sets need to be processed, in
    materials science, geosciences or engineering applications, Avizo offers
    abundant state-of-the-art image data processing, exploration and analysis
    features within an intuitive workflow and easy-to-use graphical user
    interface."""

    homepage = "https://www.thermofisher.com/sa/en/home/industrial/electron-microscopy/electron-microscopy-instruments-workflow-solutions/3d-visualization-analysis-software.html"
    version('9.7.0', '9c9b9e81957387f4218df0c5adbb80717e9ae80ab3ca6ff8da523f7f499dcc5b',
            expand=False)

    def url_for_version(self, version):
        return "file://{0}/Avizo-{1}-Linux64-gcc44.bin".format(os.getcwd(),
                                                               version.joined)

    # Licensing
    license_required = True
    license_comment = '#'
    license_files = ['share/license/password.dat']
    license_vars = ['MCSLMD_LICENSE_FILE']

    def setup_run_environment(self, env):
        env.set('MCSLMD_LICENSE_FILE', join_path(self.prefix.share.license,
                                                 'password.dat'))

    def install(self, spec, prefix):
        ver = self.version.joined
        sh = which('sh')
        sh('Avizo-{0}-Linux64-gcc44.bin'.format(ver), '--noexec', '--keep')

        with working_dir('Avizo'):
            avizo_tar = tarfile.open(name='Avizo-{0}-Linux64-gcc44.tar.bz2'
                                     .format(self.version))
            avizo_tar.extractall()

            with working_dir('Avizo-{0}'.format(self.version)):
                install_tree('bin', prefix.bin)
                install_tree('lib', prefix.lib)
                install_tree('data', prefix.data)
                install_tree('share', prefix.share)
                install_tree('python', prefix.python)
