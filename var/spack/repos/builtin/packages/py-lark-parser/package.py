# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.pkgkit import *


class PyLarkParser(PythonPackage):
    """Lark is a modern general-purpose parsing library for Python."""

    homepage = "https://github.com/lark-parser/lark/"
    pypi = "lark-parser/lark-parser-0.6.2.tar.gz"

    version('0.11.3', sha256='e29ca814a98bb0f81674617d878e5f611cb993c19ea47f22c80da3569425f9bd')
    version('0.7.1', sha256='8455e05d062fa7f9d59a2735583cf02291545f944955c4056bf1144c4e625344')
    version('0.6.2', sha256='7e2934371e0e3a5daf9afc2e3ddda76117cabcd3c3f2edf7987c1e4e9b9e503c')

    depends_on('py-setuptools', type='build')
