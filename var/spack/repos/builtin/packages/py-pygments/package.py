# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyPygments(PythonPackage):
    """Pygments is a syntax highlighting package written in Python."""

    homepage = "http://pygments.org/"
    url      = "https://pypi.io/packages/source/P/Pygments/Pygments-2.2.0.tar.gz"

    import_modules = [
        'pygments', 'pygments.filters', 'pygments.formatters',
        'pygments.lexers', 'pygments.styles'
    ]

    version('2.3.1', 'b7d04e2cd87c405938f1e494e2969814')
    version('2.2.0', '13037baca42f16917cbd5ad2fab50844')
    version('2.1.3', 'ed3fba2467c8afcda4d317e4ef2c6150')
    version('2.0.1', 'e0daf4c14a4fe5b630da765904de4d6c')
    version('2.0.2', '238587a1370d62405edabd0794b3ec4a')

    depends_on('py-setuptools', type='build')
