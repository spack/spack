# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyGensim(PythonPackage):
    """Gensim is a Python library for topic modelling, document indexing and
       similarity retrieval with large corpora. Target audience is the natural
       language processing (NLP) and information retrieval (IR) community."""

    homepage = "https://pypi.org/project/gensim/"
    url      = "https://files.pythonhosted.org/packages/3a/bc/1415be59292a23ff123298b4b46ec4be80b3bfe72c8d188b58ab2653dee4/gensim-3.8.0.tar.gz"

    version('3.8.1', sha256='33277fc0a8d7b0c7ce70fcc74bb82ad39f944c009b334856c6e86bf552b1dfdc',
            url='https://files.pythonhosted.org/packages/73/f2/e9af000df6419bf1a63ffed3e6033a1b1d8fcf2f971fcdac15296619aff8/gensim-3.8.1.tar.gz')
    version('3.8.0', sha256='ec5de7ff2bfa8692fa96a846bb5aae52f267fc322fbbe303c1f042d258af5766')

    depends_on('python@3.5:', type=('build', 'run'))

    depends_on('py-setuptools', type='build')

    depends_on('py-numpy', type=('build', 'run'))
    depends_on('py-scipy', type=('build', 'run'))
    depends_on('py-smart-open', type=('build', 'run'))
    depends_on('py-six', type=('build', 'run'))
