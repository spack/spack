# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyUriTemplate(PythonPackage):
    """RFC 6570 URI Template Processor."""

    homepage = "https://github.com/plinss/uri_template"
    pypi = "uri_template/uri_template-1.2.0.tar.gz"

    license("MIT")

    version(
        "1.2.0",
        sha256="f1699c77b73b925cf4937eae31ab282a86dc885c333f2e942513f08f691fc7db",
        url="https://pypi.org/packages/c0/db/d4f9c75b43541f7235daf4d13eb43f4491f9d5f5df45ce41daeed3a903f6/uri_template-1.2.0-py3-none-any.whl",
    )
