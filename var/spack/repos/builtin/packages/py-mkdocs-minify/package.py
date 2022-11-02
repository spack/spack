# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyMkdocsMinify(PythonPackage):
    """An MkDocs plugin to minify HTML, JS or CSS files prior to being written to disk."""

    pypi = "mkdocs-minify-plugin/mkdocs-minify-plugin-0.6.1.tar.gz"

    #maintainers = ["wscullin"]

    version("0.6.1", sha256="29e14e4ab2d436cb05f56333c9bfbff561fc89402e04d0f1ccfe23a3e7070ba2")

    depends_on('python@3.7:', type=('build', 'run'))

    depends_on('py-mkdocs@1.4.1:', type=('build', 'run'))
    depends_on('py-htmlmin', type=('build', 'run'))
    depends_on('py-jsmin@3.0.1:', type=('build', 'run'))
    depends_on('py-csscompressor', type=('build', 'run'))
