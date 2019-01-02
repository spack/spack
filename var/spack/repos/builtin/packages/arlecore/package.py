# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Arlecore(Package):
    """An Integrated Software for Population Genetics Data Analysis"""

    homepage = "http://cmpg.unibe.ch/software/arlequin35/"
    url      = "http://cmpg.unibe.ch/software/arlequin35/linux/arlecore_linux.zip"

    version('3.5.2.2', '347a589fc609f359eb61557a2e8ceb2f')

    depends_on('r', type=('build', 'run'))

    def install(self, spec, prefix):
        install_tree('.', prefix)
