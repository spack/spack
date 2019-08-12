# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyFastaindex(PythonPackage):
    """FastA index (.fai) handler compatible with samtools faidx is extended
       with 4 columns storing counts for A, C, G & T for each sequence.."""

    homepage = "https://github.com/lpryszcz/FastaIndex"
    url      = "https://pypi.io/packages/source/F/FastaIndex/FastaIndex-0.11rc7.tar.gz"

    version('0.11rc7', '882c973d968d9db596edfd0fbb07e3a8')

    depends_on('py-setuptools', type='build')
