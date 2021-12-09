# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyFlawfinder(PythonPackage):
    """a program that examines source code looking for security weaknesses"""

    homepage = "http://dwheeler.com/flawfinder/"

    version('2.0.19', sha256='f18f0021d9a2f3ffc1c1e32aa7bb1bb5ca1bad91b82b32157f44e5d0a1a23ad0',
            url='https://files.pythonhosted.org/packages/98/64/32f24ec56ea8603ccfc471549de2fb9957613fba75315e121108a9b80b51/flawfinder-2.0.19-py2.py3-none-any.whl',
            expand=False)

    depends_on('python@2.7:', type=('build', 'run'))
    depends_on('py-pip',      type='build')
    depends_on('py-wheel',    type='build')

    phases = ['install']

    # copied from py-azureml-core
    def install(self, spec, prefix):
        pip = which('pip')
        pip('install', '--no-deps', self.stage.archive_file,
            '--prefix={0}'.format(prefix))
