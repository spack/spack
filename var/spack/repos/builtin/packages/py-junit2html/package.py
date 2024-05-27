# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyJunit2html(PythonPackage):
    """
    Simple self-contained python tool to produce a single html file from a single junit xml file.
    """

    homepage = "https://gitlab.com/inorton/junit2html"

    pypi = "junit2html/junit2html-31.0.2-py3-none-any.whl"

    maintainers("LydDeb")

    version("31.0.2", sha256="c7fd1f253d423f0df031d0cee8ef7d4d98d9f8bf6383a2d40dca639686814866")
