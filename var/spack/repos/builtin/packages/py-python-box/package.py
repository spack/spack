# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyPythonBox(PythonPackage):
    """Advanced Python dictionaries with dot notation access

    Box will automatically make otherwise inaccessible keys safe to access as
    an attribute. You can always pass conversion_box=False to Box to disable
    that behavior. Also, all new dict and lists added to a Box or BoxList
    object are converted automatically."""

    homepage = "https://github.com/cdgriffith/Box"
    pypi = "python-box/python-box-5.3.0.tar.gz"

    license("MIT")

    version(
        "5.3.0",
        sha256="f2a531f9f5bbef078c175fad6abb31e9b59d40d121ea79993197e6bb221c6be6",
        url="https://pypi.org/packages/ae/55/b81be1c1456d93db93905b364d19cac5dde22fb8f442b42d41087c2fe28f/python_box-5.3.0-py3-none-any.whl",
    )

    variant("extras", default=False, description='install the "extras" packages')
