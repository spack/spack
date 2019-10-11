# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyDocutils(PythonPackage):
    """Docutils is an open-source text processing system for processing
    plaintext documentation into useful formats, such as HTML, LaTeX,
    man-pages, open-document or XML. It includes reStructuredText, the
    easy to read, easy to use, what-you-see-is-what-you-get plaintext
    markup language."""

    homepage = "http://docutils.sourceforge.net/"
    url      = "https://pypi.io/packages/source/d/docutils/docutils-0.13.1.tar.gz"

    import_modules = [
        'docutils', 'docutils.languages', 'docutils.parsers',
        'docutils.readers', 'docutils.transforms', 'docutils.utils',
        'docutils.writers', 'docutils.parsers.rst',
        'docutils.parsers.rst.directives', 'docutils.parsers.rst.languages',
        'docutils.utils.math', 'docutils.writers.html4css1',
        'docutils.writers.html5_polyglot', 'docutils.writers.latex2e',
        'docutils.writers.odf_odt', 'docutils.writers.pep_html',
        'docutils.writers.s5_html', 'docutils.writers.xetex'
    ]

    version('0.14', sha256='51e64ef2ebfb29cae1faa133b3710143496eca21c530f3f71424d77687764274')
    version('0.13.1', sha256='718c0f5fb677be0f34b781e04241c4067cbd9327b66bdd8e763201130f5175be')
    version('0.12',   sha256='c7db717810ab6965f66c8cf0398a98c9d8df982da39b4cd7f162911eb89596fa')
