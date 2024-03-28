# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyChainmap(PythonPackage):
    """Clone/backport of ChainMap for Python 2.6, Python 3.2, and PyPy3
    based on Python 3.2--versions that currently lack their own
    ChainMap implementations."""

    homepage = "https://bitbucket.org/jeunice/chainmap/src/default/"
    pypi = "chainmap/chainmap-1.0.3.tar.gz"

    version(
        "1.0.3",
        sha256="22b6ccf38698c0356e65e5dfa49c98fb16e3408928b95d90e2332e2fb787988e",
        url="https://pypi.org/packages/f5/f7/78ddc379d5dc2bbdcf690c3663396d8be5f2c7bc76d30012beef620272ee/chainmap-1.0.3-py3-none-any.whl",
    )
    version(
        "1.0.2",
        sha256="b13329fca4a46a458dd5d5de8ee1ae94f034a2c13a17f9149478941d043eef8b",
        url="https://pypi.org/packages/6a/53/795ce18439a067eea1b233152985c0e67fd7dcc4edf102fb30f8cca6bad0/chainmap-1.0.2-py2.py3-none-any.whl",
    )
    version(
        "1.0.1",
        sha256="d14574cf97732161d25d07ccb06c83b95ce79b9c9da1cc4f958b43c5ed72efc6",
        url="https://pypi.org/packages/27/bd/3599f48eaf21e760230e55b48e0e319c5753c010c5a4905b899f7dd118f2/chainmap-1.0.1-py2.py3-none-any.whl",
    )
    version(
        "1.0.0",
        sha256="be7e2b8eefeed54dfad7fd33b0b13f6d6408303c08dd677a73232aefeabde89c",
        url="https://pypi.org/packages/99/7c/17181804025a457477bf361b4fcecbefdfd564326c1f1dccc5e30ef2bc57/chainmap-1.0.0-py2.py3-none-any.whl",
    )
