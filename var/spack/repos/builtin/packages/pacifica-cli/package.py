# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PacificaCli(PythonPackage):
    """Python CLI for Pacifica Core Services"""

    homepage = "https://github.com/pacifica/pacifica-cli/"
    url = "https://pypi.io/packages/source/p/pacifica-cli/pacifica-cli-0.5.2.tar.gz"

    version('0.5.2', sha256='fee5fa8ac38ffec2e9199bff23afbbae697c4f7554f13e340104f8b20a62843f')

    depends_on('py-setuptools', type='build')
    depends_on('py-wheel', type='build')
    depends_on('py-importlib-metadata', type='run')
    depends_on('py-jsonschema', type='run')
    depends_on('py-pacifica-uploader@0.3.1:0.3.9999', type='run')
    depends_on('py-pacifica-downloader@0.4.1:0.4.9999', type='run')
    depends_on('py-pacifica-namespace', type='run')
    depends_on('py-pager', type='run')
    depends_on('python@3:', type=('build', 'run'))
