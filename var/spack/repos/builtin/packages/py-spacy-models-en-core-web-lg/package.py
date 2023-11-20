# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PySpacyModelsEnCoreWebLg(PythonPackage):
    """English pipeline optimized for CPU. Components: tok2vec, tagger, parser,
    senter, ner, attribute_ruler, lemmatizer."""

    homepage = "https://spacy.io/models/en#en_core_web_lg"
    url = "https://github.com/explosion/spacy-models/releases/download/en_core_web_lg-3.5.0/en_core_web_lg-3.5.0.tar.gz"

    version("3.5.0", sha256="29732c8167e444686e0d8716d6b09123f3fa2d32baf7dbd2d8bc6c1b2c1b6945")

    depends_on("py-setuptools", type="build")
    depends_on("py-spacy@3.5", when="@3.5", type=("build", "run"))
