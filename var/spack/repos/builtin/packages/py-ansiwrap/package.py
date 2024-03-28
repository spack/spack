# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyAnsiwrap(PythonPackage):
    """textwrap, but savvy to ANSI colors and styles."""

    homepage = "https://github.com/jonathaneunice/ansiwrap"
    pypi = "ansiwrap/ansiwrap-0.8.4.zip"

    license("Apache-2.0")

    version(
        "0.8.4",
        sha256="7b053567c88e1ad9eed030d3ac41b722125e4c1271c8a99ade797faff1f49fb1",
        url="https://pypi.org/packages/03/50/43e775a63e0d632d9be3b3fa1c9b2cbaf3b7870d203655710a3426f47c26/ansiwrap-0.8.4-py2.py3-none-any.whl",
    )
