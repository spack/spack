# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class PyEnumTools(PythonPackage):
    """Tools to expand Python's enum module."""

    homepage = "https://github.com/domdfcoding/enum_tools"
    pypi = "enum_tools/enum_tools-0.10.0.tar.gz"

    license("LGPL-3.0-or-later")

    version(
        "0.10.0",
        sha256="87f4e8216468e53f2920d2e016dc18eea0972b0b6c1eea65756fbc331a3113d2",
        url="https://pypi.org/packages/5e/ff/32606deb6780b56ac9e6749c697db3db261e4549a4b873b72f983722ead8/enum_tools-0.10.0-py3-none-any.whl",
    )

    with default_args(type="run"):
        depends_on("py-pygments@2.6.1:")
        depends_on("py-typing-extensions@3.7.4.3:")
