# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyLatexcodec(PythonPackage):
    """A lexer and codec to work with LaTeX code in Python."""

    homepage = "http://latexcodec.readthedocs.io"
    pypi = "latexcodec/latexcodec-1.0.4.tar.gz"

    version('2.0.1', sha256='2aa2551c373261cefe2ad3a8953a6d6533e68238d180eb4bb91d7964adb3fe9a')
    version('2.0.0', sha256='cd3f649d489169ed593f9466ef6ba485e694f6871d9696601e78307b5b84df5f')
    version('1.0.7', sha256='ebc183904549b1514ffc29a8768c8b58dc45cb813b94df90bf19f4c7b01fd772')
    version('1.0.6', sha256='01ad6b8d99606bb902f94269d6a14597000d220885781087bc880a0ede6a9c68')
    version('1.0.5', sha256='9607d9d260654eb607c54a8b8c991e4406008605c383ded4f4034522dc0bad7d')
    version('1.0.4', sha256='62bf8a3ee298f169a4d014dad5522bc1325b54dc98789a453fd338620387cb6c')

    depends_on('py-setuptools', type='build')
    depends_on('py-six@1.4.1:', type=('build', 'run'))
