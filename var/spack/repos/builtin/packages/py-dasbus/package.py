# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyDasbus(PythonPackage):
    """Dasbus is a DBus library written in Python 3, based on GLib and inspired by pydbus."""

    homepage = "https://dasbus.readthedocs.io/en/latest/"
    pypi = "dasbus/dasbus-1.7.tar.gz"
    license("LGPL-2.1-or-later")

    version(
        "1.7",
        sha256="0a9433e9e72c2c865fa2d5ef824ac4ef49b540cf57f6396e515c2f314e5c14cd",
        url="https://pypi.org/packages/e1/b4/4d55b9359bc34d56b29b943b378331dd8aaea6db6d0543e5d97fed4b1af7/dasbus-1.7-py3-none-any.whl",
    )
