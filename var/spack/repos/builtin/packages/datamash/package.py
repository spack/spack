# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Datamash(AutotoolsPackage):
    """GNU datamash is a command-line program which performs basic numeric,
    textual and statistical operations on input textual data files.
    """

    homepage = "https://www.gnu.org/software/datamash/"
    url      = "https://ftpmirror.gnu.org/datamash/datamash-1.0.5.tar.gz"

    version('1.3',   '47d382090e367ddb4967d640aba77b66')
    version('1.1.0', '79a6affca08107a095e97e4237fc8775')
    version('1.0.7', '9f317bab07454032ba9c068e7f17b04b')
    version('1.0.6', 'ff26fdef0f343cb695cf1853e14a1a5b')
    version('1.0.5', '9a29549dc7feca49fdc5fab696614e11')

    build_directory = 'spack-build'
