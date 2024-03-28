# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PySetuptoolsScmGitArchive(PythonPackage):
    """This is a setuptools_scm plugin that adds support for git archives
    (for example the ones GitHub automatically generates)."""

    homepage = "https://github.com/Changaco/setuptools_scm_git_archive/"
    pypi = "setuptools_scm_git_archive/setuptools_scm_git_archive-1.1.tar.gz"

    maintainers("marcmengel")

    license("MIT")

    version(
        "1.4",
        sha256="600cd90b420bec4802ce3843d5b52c9dc618fc7d9826e245f8d6f091c5944279",
        url="https://pypi.org/packages/3f/35/7189a677393f32555d3574d131894b824ce277bd79e8e2bb3713e4c08c10/setuptools_scm_git_archive-1.4-py2.py3-none-any.whl",
    )
    version(
        "1.1",
        sha256="3df19d1f05f70bb4b33485a88669726f1b2f14600ef2e557b927fc9cbdbfff2b",
        url="https://pypi.org/packages/7e/83/284c6d3fac2e74532a9f51f908018690709db9af1469cf728574f6be3abf/setuptools_scm_git_archive-1.1-py2.py3-none-any.whl",
    )
    version(
        "1.0",
        sha256="af6b40a3f2f6d79b2b6b495258ff441641908ff2c4c9aaa66765b87ec6f72c35",
        url="https://pypi.org/packages/24/fc/42b5d0d6ea83d51fcd1a2a01ef056bec58414996c6342cda72bdd92e700d/setuptools_scm_git_archive-1.0-py2.py3-none-any.whl",
    )
