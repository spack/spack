# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyAioitertools(Package):
    """Implementation of itertools, builtins, and more for AsyncIO and mixed-type iterables."""

    homepage = "https://aioitertools.omnilib.dev/en/stable/"
    url      = "https://files.pythonhosted.org/packages/32/0b/3260ac050de07bf6e91871944583bb8598091da19155c34f7ef02244709c/aioitertools-0.7.1-py3-none-any.whl"

    version('0.7.1' , sha256='8972308474c41ed5e0636819f948ebff32f2318e70f7e7d23cd208c4357cc773', expand=False)

    extends('python')
    depends_on('python@3.6:3.7.999', type=('build', 'run'))
    depends_on('py-typing-extensions@3.7:', type=('build', 'run'))
    depends_on('py-pip',             type=('build'))

    def install(self, spec, prefix):
        pip = which('pip')
        pip('install', self.stage.archive_file, '--prefix={0}'.format(prefix))
