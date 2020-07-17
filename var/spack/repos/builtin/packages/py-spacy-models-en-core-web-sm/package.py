# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


class PySpacyModelsEnCoreWebSm(PythonPackage):
    """English multi-task CNN trained on OntoNotes. Assigns context-specific
    token vectors, POS tags, dependency parse and named entities."""

    homepage = "https://spacy.io/models/en#en_core_web_sm"
    url      = "https://github.com/explosion/spacy-models/releases/download/en_core_web_sm-2.2.5/en_core_web_sm-2.2.5.tar.gz"

    version('2.2.5', sha256='60b69065c97fd2e4972c33300205e1dead3501d2e0bfd6a182c3a033e337caee')

    depends_on('py-setuptools', type='build')
    depends_on('py-spacy@2.2.2:', type=('build', 'run'))
