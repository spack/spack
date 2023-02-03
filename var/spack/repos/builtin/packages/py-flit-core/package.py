# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyFlitCore(Package, PythonExtension):
    """Distribution-building parts of Flit."""

    homepage = "https://github.com/takluyver/flit"
    # Must be installed from wheel to avoid circular dependency on build
    url = "https://files.pythonhosted.org/packages/py3/f/flit-core/flit_core-3.8.0-py3-none-any.whl"
    list_url = "https://pypi.org/simple/flit-core/"

    maintainers("takluyver")

    version("3.8.0", sha256="64a29ec845164a6abe1136bf4bc5ae012bdfe758ed42fc7571a9059a7c80bd83", expand=False)

    extends("python")
    depends_on("py-installer", type="build")

    def install(self, spec, prefix):
        installer("--prefix", prefix, self.stage.archive_file)
