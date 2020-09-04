# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


class PyNltk(PythonPackage):
    """The Natural Language Toolkit (NLTK) is a Python package for
    natural language processing."""

    homepage = "https://www.nltk.org/"
    url      = "https://pypi.io/packages/source/n/nltk/nltk-3.5.zip"

    version('3.5', sha256='845365449cd8c5f9731f7cb9f8bd6fd0767553b9d53af9eb1b3abf7700936b35')

    variant('data', default=False, description='Download the NLTK data')

    depends_on('python@3.5:', type=('build', 'run'))
    depends_on('py-setuptools', type=('build', 'run'))
    depends_on('py-click', type=('build', 'run'))
    depends_on('py-regex', type=('build', 'run'))
    depends_on('py-tqdm', type=('build', 'run'))
    depends_on('py-importlib-metadata', type=('build', 'run'))

    def setup_run_environment(self, run_env):
        if '+data' in self.spec:
            run_env.prepend_path("NLTK_DATA", self.prefix.data)

    @run_after('install')
    def install_data(self):
        if '+data' in self.spec:
            mkdirp(prefix.data)
            python('-m',
                   'nltk.downloader',
                   '-d',
                   prefix.data,
                   'all')

    # May require additional third-party software:
    # https://github.com/nltk/nltk/wiki/Installing-Third-Party-Software
