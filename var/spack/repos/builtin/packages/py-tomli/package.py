# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyTomli(PythonPackage):
    """Tomli is a Python library for parsing TOML.

    Tomli is fully compatible with TOML v1.0.0."""

    homepage = "https://github.com/hukkin/tomli"
    pypi = "tomli/tomli-1.2.1.tar.gz"

    version('1.2.2', sha256='c6ce0015eb38820eaf32b5db832dbc26deb3dd427bd5f6556cf0acac2c214fee')
    version('1.2.1', sha256='a5b75cb6f3968abb47af1b40c1819dc519ea82bcc065776a866e8d74c5ca9442')

    depends_on('python@3.6:', type=('build', 'run'))

    resource(
        name='flit-core',
        url='https://files.pythonhosted.org/packages/source/f/flit-core/flit_core-3.5.1.tar.gz',
        sha256='3083720351a6cb00e0634a1ec0e26eae7b273174c3c6c03d5b597a14203b282e',
        placement='flit-core',
    )

    def setup_build_environment(self, env):
        # tomli is built using flit-core, but flit-core has a run-time dep on tomli
        env.prepend_path('PYTHONPATH', '.')
        env.prepend_path('PYTHONPATH', join_path(self.stage.source_path, 'flit-core'))
