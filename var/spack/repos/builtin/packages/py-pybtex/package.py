# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack import *


class PyPybtex(PythonPackage):
    """Pybtex is a BibTeX-compatible bibliography processor written in
       Python."""

    homepage = "https://pybtex.org"
    pypi = "Pybtex/pybtex-0.21.tar.gz"

    version('0.24.0', sha256='818eae35b61733e5c007c3fcd2cfb75ed1bc8b4173c1f70b56cc4c0802d34755')
    version('0.23.0', sha256='b92be18ccd5e9a37895949dcf359a1f6890246b73646dddf1129178ee12e4bef')
    version('0.22.2', sha256='00816e5f8570609d8ce3360cd23916bd3e50428a3508127578fdb4dc2b731c1c')
    version('0.22.1', sha256='bc6aaf8c5b56c9c5cfe34fd4171295c2b637193d2265b02c10db5608aec11aba')
    version('0.22.0', sha256='26b70ec9f941db330c198fe1f2743182e9d8c2afa0a4b8ccca695f11e079f966')
    version('0.21', sha256='af8a6c7c74954ad305553b118d2757f68bc77c5dd5d5de2cc1fd16db90046000')

    depends_on('py-setuptools', type='build')
    depends_on('py-latexcodec@1.0.4:', type=('build', 'run'))
    depends_on('py-pyyaml@3.01:', type=('build', 'run'))
    depends_on('py-counter@1:', when='^python@:2.6', type=('build', 'run'))
