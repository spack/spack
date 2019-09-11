@@ -0,0 +1,36 @@
# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
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
    features within an intuitive workflow and easy-to-use graphical user interface."""

    homepage = "https://www.thermofisher.com/sa/en/home/industrial/electron-microscopy/\
               electron-microscopy-instruments-workflow-solutions/3d-visualization-\
               analysis-software.html"
    version('9.7.0', 'ed3947e61a1d17839005c824df975030')

    ## You have to create the tarball for the source code to be processed correctly.
    def url_for_version(self, version):
        return "file://{0}/avizo_{1}_linux64_gcc44.tar.gz".format(os.getcwd(), version)

    def install(self, spec, prefix):
        ver = str(self.version).replace(".", "")
        os.system('sh Avizo-{0}-Linux64-gcc44.bin --noexec --keep'.format(ver))

        os.chdir(join_path(self.stage.source_path, 'Avizo'))
        avizo_tar = tarfile.open(name='Avizo-{0}-Linux64-gcc44.tar.bz2'.format(self.version))
        avizo_tar.extractall()

        install_tree(join_path(self.stage.source_path, 'Avizo/Avizo-{0}'.format(self.version)), prefix)
        intsall('file://{0}/password.dat'.format(os.getcwd()), join_path(prefix, 'share/license')
