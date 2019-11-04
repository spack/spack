# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyTatsu(PythonPackage):
    """竜 TatSu (the successor to Grako) is a tool that takes grammars in
    a variation of EBNF as input, and outputs memoizing (Packrat) PEG
    parsers in Python."""

    homepage = "https://github.com/neogeny/tatsu"
    url      = "https://pypi.io/packages/source/T/TatSu/TatSu-4.4.0.zip"

    version('4.4.0', sha256='80713413473a009f2081148d0f494884cabaf9d6866b71f2a68a92b6442f343d')

    depends_on('py-setuptools', type='build')
    depends_on('py-colorama@0.4:', type=('build', 'run'))
    depends_on('py-dataclasses@0.6:', type=('build', 'run'), when='^python@3.6.0:3.6.99')
    depends_on('py-mypy@0.641:', type=('build', 'run'))
    depends_on('py-pyyaml@3.12:', type=('build', 'run'))
    depends_on('py-regex@2018.8:', type=('build', 'run'))
    depends_on('py-typing@3.6:', type=('build', 'run'), when='^python@:3.4.99')
