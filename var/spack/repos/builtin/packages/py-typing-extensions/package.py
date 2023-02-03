# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyTypingExtensions(Package, PythonExtension):
    """Backported and Experimental Type Hints for Python 3.7+."""

    homepage = "https://github.com/python/typing_extensions"
    # Must be installed from wheel to avoid circular dependency on build
    url = "https://files.pythonhosted.org/packages/py3/t/typing-extensions/typing_extensions-4.4.0-py3-none-any.whl"
    list_url = "https://pypi.org/simple/typing-extensions/"

    version("4.4.0", sha256="16fa4864408f655d35ec496218b85f79b3437c829e93320c7c9215ccfd92489e", expand=False)
    version("4.3.0", sha256="25642c956049920a5aa49edcdd6ab1e06d7e5d467fc00e0506c44ac86fbfca02", expand=False)
    version("4.2.0", sha256="6657594ee297170d19f67d55c05852a874e7eb634f4f753dbd667855e07c1708", expand=False)
    version("4.1.1", sha256="21c85e0fe4b9a155d0799430b0ad741cdce7e359660ccbd8b530613e8df88ce2", expand=False)
    version("3.10.0.2", sha256="f1d25edafde516b146ecd0613dabcc61409817af4766fbbcfb8d1ad4ec441a34", expand=False)
    version("3.10.0.0", sha256="779383f6086d90c99ae41cf0ff39aac8a7937a9283ce0a414e5dd782f4c94a84", expand=False)
    version("3.7.4", sha256="d8179012ec2c620d3791ca6fe2bf7979d979acdbef1fca0bc56b37411db682ed", expand=False)
    version("3.7.2", sha256="f3f0e67e1d42de47b5c67c32c9b26641642e9170fe7e292991793705cd5fef7c", expand=False)
    version("3.6.6", sha256="55401f6ed58ade5638eb566615c150ba13624e2f0c1eedd080fc3c1b6cb76f1d", expand=False)

    extends("python")
    depends_on("py-installer", type="build")

    def install(self, spec, prefix):
        installer("--prefix", prefix, self.stage.archive_file)
