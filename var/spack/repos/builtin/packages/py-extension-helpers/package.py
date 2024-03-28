# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package import *


class PyExtensionHelpers(PythonPackage):
    """The extension-helpers package includes convenience helpers to
    assist with building Python packages with compiled C/Cython
    extensions. It is developed by the Astropy project but is intended
    to be general and usable by any Python package."""

    homepage = "https://github.com/astropy/astropy-helpers"
    pypi = "extension-helpers/extension-helpers-0.1.tar.gz"

    license("BSD-3-Clause")

    version(
        "0.1",
        sha256="f641ec85823dfe623013981c11dbb07c158d10afd5bc8a11e6cf3aa1d764aca9",
        url="https://pypi.org/packages/7e/45/83c124b7dbfefcf0ccb3b6672e199e3e17c04a9a34f3a34618ca64e16da7/extension_helpers-0.1-py2.py3-none-any.whl",
    )
