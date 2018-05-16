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


class RdpClassifier(Package):
    """The RDP Classifier is a naive Bayesian classifier that can rapidly and
       accurately provides taxonomic assignments from domain to genus, with
       confidence estimates for each assignment. """

    homepage = "http://rdp.cme.msu.edu/"
    url      = "https://downloads.sourceforge.net/project/rdp-classifier/rdp-classifier/rdp_classifier_2.12.zip"

    version('2.12', '7fdfa33512629810f0ff06b905642ddd')

    depends_on('java', type=('build', 'run'))

    def install(self, spec, prefix):
        mkdirp(prefix.bin)
        install(join_path('dist', 'classifier.jar'), prefix.bin)
        install_tree(join_path('dist', 'lib'), prefix.bin.lib)
        install(join_path('lib', 'junit-4.8.2.jar'), prefix.bin.lib)
        install_tree('src', prefix.src)
