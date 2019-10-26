# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyMethylcode(PythonPackage):
    """MethylCoder is a single program that takes of bisulfite-treated
       reads and outputs per-base methylation data. """

    homepage = "https://github.com/brentp/methylcode"
    url      = "https://github.com/brentp/methylcode/archive/master.zip"

    version('1.0.0', sha256='30f707a690a887e3161c8debba3c322bd313865df40212275b02203c52a416ae')

    depends_on('python@2.7.0:2.7.999')
    depends_on('py-six')
    depends_on('py-setuptools')
    depends_on('py-numpy')
    depends_on('py-pyparsing')
    depends_on('py-pyfasta')
    depends_on('py-bsddb3')
    depends_on('bowtie')
