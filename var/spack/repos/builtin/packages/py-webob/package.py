# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyWebob(PythonPackage):
    """WebOb provides objects for HTTP requests and responses."""

    homepage = "https://webob.org/"
    pypi = "WebOb/WebOb-1.8.7.tar.gz"

    license("MIT")

    version(
        "1.8.7",
        sha256="73aae30359291c14fa3b956f8b5ca31960e420c28c1bec002547fb04928cf89b",
        url="https://pypi.org/packages/62/9c/e94a9982e9f31fc35cf46cdc543a6c2c26cb7174635b5fd25b0bbc6a7bc0/WebOb-1.8.7-py2.py3-none-any.whl",
    )
