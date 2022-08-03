# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyAsttokens(PythonPackage):
    """Annotate AST trees with source code positions."""

    homepage = "https://github.com/gristlabs/asttokens"
    pypi     = "asttokens/asttokens-2.0.5.tar.gz"

    version('2.0.5', sha256='9a54c114f02c7a9480d56550932546a3f1fe71d8a02f1bc7ccd0ee3ee35cf4d5')

    depends_on('py-setuptools@44:', type='build')
    depends_on('py-setuptools-scm+toml@3.4.3:', type='build')

    depends_on('py-six', type=('build', 'run'))
