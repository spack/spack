# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PySetuptoolsGit(PythonPackage):
    """Setuptools revision control system plugin for Git"""

    pypi = "setuptools-git/setuptools-git-1.2.tar.gz"

    license("BSD-3-Clause")

    version(
        "1.2",
        sha256="e7764dccce7d97b4b5a330d7b966aac6f9ac026385743fd6cedad553f2494cfa",
        url="https://pypi.org/packages/05/97/dd99fa9c0d9627a7b3c103a00f1566d8193aca8d473884ed258cca82b06f/setuptools_git-1.2-py2.py3-none-any.whl",
    )
