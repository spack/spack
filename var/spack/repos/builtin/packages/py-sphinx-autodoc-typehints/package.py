# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


class PySphinxAutodocTypehints(PythonPackage):
    """
    Type hints (PEP 484) support for the Sphinx autodoc extension
    """

    homepage = ""
    pypi      = "sphinx-autodoc-typehints/sphinx-autodoc-typehints-1.12.0.tar.gz"

    version('1.9.0', sha256='0dfd26be5b81049ce81b644913a06a12795ded2791adc0a4e13420eb9a832852')

    depends_on('python@3.6:', type=('build', 'run'))
    depends_on('py-setuptools@36.2.7:', type='build')
    depends_on('py-setuptools-scm@1.7.0:', type='build')
    depends_on('py-sphinx@3.2.0:', type='build')
    depends_on('py-dataclasses', type=('test', 'run'))
    depends_on('py-pytest@3.1.0:', type=('test', 'run'))
    depends_on('py-sphobjinv@2.0:', type=('test', 'run'))
    depends_on('py-typing-extensions@3.5:', type=('test', 'run'))
    depends_on('py-typed-ast', type=('test', 'run'))
