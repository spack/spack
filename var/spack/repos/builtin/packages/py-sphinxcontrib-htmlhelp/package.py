# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PySphinxcontribHtmlhelp(PythonPackage):
    """sphinxcontrib-htmlhelp is a sphinx extension which outputs htmlhelp
    document."""

    homepage = "http://sphinx-doc.org/"
    pypi = "sphinxcontrib-htmlhelp/sphinxcontrib-htmlhelp-1.0.2.tar.gz"

    # 'sphinx' requires 'sphinxcontrib-htmlhelp' at build-time, but
    # 'sphinxcontrib-htmlhelp' requires 'sphinx' at run-time. Don't bother trying to
    # import any modules.
    import_modules = []

    version('2.0.0', sha256='f5f8bb2d0d629f398bf47d0d69c07bc13b65f75a81ad9e2f71a63d4b7a2f6db2')
    version('1.0.2', sha256='4670f99f8951bd78cd4ad2ab962f798f5618b17675c35c5ac3b2132a14ea8422')

    depends_on('python@3.6:', when='@2:', type=('build', 'run'))
    depends_on('python@3.5:', type=('build', 'run'))
    depends_on('py-setuptools', type='build')
