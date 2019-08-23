# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyRuamelYaml(PythonPackage):
    """"""

    homepage = "https://bitbucket.org/ruamel/yaml/src/default/"
    url      = "https://pypi.io/packages/source/r/ruamel.yaml/ruamel.yaml-0.16.5.tar.gz"

    version('0.16.5', sha256='412a6f5cfdc0525dee6a27c08f5415c7fd832a7afcb7a0ed7319628aed23d408')

    depends_on('py-setuptools', type='build')
    # depends_on('py-foo',        type=('build', 'run'))

    def build_args(self, spec, prefix):
        # FIXME: Add arguments other than --prefix
        # FIXME: If not needed delete this function
        args = []
        return args
