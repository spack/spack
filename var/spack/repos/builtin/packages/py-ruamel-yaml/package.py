# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyRuamelYaml(PythonPackage):
    """
    a YAML parser/emitter that supports roundtrip preservation of comments,
    seq/map flow style, and map key order
    """

    homepage = "https://bitbucket.org/ruamel/yaml/src/default/"
    url      = "https://pypi.io/packages/source/r/ruamel.yaml/ruamel.yaml-0.16.5.tar.gz"

    version('0.16.5', sha256='412a6f5cfdc0525dee6a27c08f5415c7fd832a7afcb7a0ed7319628aed23d408')
    version('0.11.7', sha256='c89363e16c9eafb9354e55d757723efeff8682d05e56b0881450002ffb00a344')

    depends_on('py-setuptools', type='build')

    @run_after('install')
    def fix_import_error(self):
        if str(self.spec['python'].version.up_to(1)) == '2':
            touch = which('touch')
            touch(self.prefix + '/' +
                  self.spec['python'].package.site_packages_dir +
                  '/ruamel/__init__.py')
