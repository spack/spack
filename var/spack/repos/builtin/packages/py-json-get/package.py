# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyJsonGet(PythonPackage):
    """Get values from JSON objects usings a path expression."""

    homepage = "https://github.com/srittau/python-json-get"
    url = "https://github.com/srittau/python-json-get/archive/v1.1.1.tar.gz"

    license("MIT")

    version(
        "1.1.1",
        sha256="884854fb225aa72e2a975dc545704f93e1f87f9377108c27fa27b0c0cca92374",
        url="https://pypi.org/packages/fe/f6/a8fe09ed8b3db17ceb41ae21e54923256402c3fca90d8874fe9216721ae9/json_get-1.1.1-py3-none-any.whl",
    )
