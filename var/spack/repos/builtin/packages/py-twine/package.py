# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyTwine(PythonPackage):
    """Twine is a utility for publishing Python packages on PyPI."""

    homepage = "https://twine.readthedocs.io/"
    pypi = "twine/twine-2.0.0.tar.gz"

    version('3.3.0', sha256='fcffa8fc37e8083a5be0728371f299598870ee1eccc94e9a25cef7b1dcfa8297')
    version('3.2.0', sha256='34352fd52ec3b9d29837e6072d5a2a7c6fe4290e97bba46bb8d478b5c598f7ab')
    version('3.1.1', sha256='d561a5e511f70275e5a485a6275ff61851c16ffcb3a95a602189161112d9f160')
    version('3.1.0', sha256='1a87ae3f1e29a87a8ac174809bf0aa996085a0368fe500402196bda94b23aab3')
    version('3.0.0', sha256='8d85e75338c97ea7ed04330b1dce1d948ce83cec333fb9a0e26a11ffdc4a40dd')
    version('2.0.0', sha256='9fe7091715c7576df166df8ef6654e61bada39571783f2fd415bdcba867c6993')

    depends_on('python@3.6:', type=('build', 'run'))
    depends_on('py-pkginfo@1.4.2:', type=('build', 'run'))
    depends_on('py-readme-renderer@21.0:', type=('build', 'run'))
    depends_on('py-requests-toolbelt@0.8.0:0.8.999,0.9.1:', type=('build', 'run'))
    depends_on('py-setuptools@0.7.0:', type=('build', 'run'))
    depends_on('py-tqdm@4.14:', type=('build', 'run'))
