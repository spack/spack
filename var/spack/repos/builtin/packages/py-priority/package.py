# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyPriority(PythonPackage):
    """Priority is a pure-Python implementation of the priority
    logic for HTTP/2, set out in RFC 7540 Section 5.3 (Stream
    Priority). This logic allows for clients to express a
    preference for how the server allocates its (limited)
    resources to the many outstanding HTTP requests that may be
    running over a single HTTP/2 connection."""

    homepage = "https://github.com/python-hyper/priority/"
    pypi = "priority/priority-2.0.0.tar.gz"

    license("MIT")

    version(
        "2.0.0",
        sha256="6f8eefce5f3ad59baf2c080a664037bb4725cd0a790d53d59ab4059288faf6aa",
        url="https://pypi.org/packages/5e/5f/82c8074f7e84978129347c2c6ec8b6c59f3584ff1a20bc3c940a3e061790/priority-2.0.0-py3-none-any.whl",
    )
