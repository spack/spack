# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyXrootdpyfs(PythonPackage):
    """XRootDPyFS is a PyFilesystem interface to XRootD."""

    homepage = "http://github.com/inveniosoftware/xrootdpyfs/"
    pypi = "xrootdpyfs/xrootdpyfs-0.2.2.tar.gz"

    version(
        "0.2.2",
        sha256="c2fae96c7e8039c274aa5acc606cabc11648a20afa9aaabb275e01d69961e082",
        url="https://pypi.org/packages/ae/2c/069484b2d26518bfbc9e4488371fbfa196e45e89f8f0f76c99727bdbc46d/xrootdpyfs-0.2.2-py2.py3-none-any.whl",
    )

    with default_args(type="run"):
        depends_on("py-fs@0.5.4:0", when="@0.2.2:0")
        depends_on("py-xrootd@:4", when="@0.2.2:1")
