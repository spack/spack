# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PySpacyLoggers(PythonPackage):
    """Logging utilities for SpaCy"""

    homepage = "https://github.com/explosion/spacy-loggers"
    pypi = "spacy-loggers/spacy-loggers-1.0.4.tar.gz"

    license("MIT")

    version(
        "1.0.4",
        sha256="e050bf2e63208b2f096b777e494971c962ad7c1dc997641c8f95c622550044ae",
        url="https://pypi.org/packages/62/8c/814e0bd139a8c94b50298be3a4e640d90cdce78efe0099e373a767b7d854/spacy_loggers-1.0.4-py3-none-any.whl",
    )
