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

    extends("python")
    depends_on("py-installer", type="build")

    def install(self, spec, prefix):
        installer("--prefix", prefix, self.stage.archive_file)
