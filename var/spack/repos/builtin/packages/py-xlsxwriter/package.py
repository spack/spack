# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyXlsxwriter(PythonPackage):
    """XlsxWriter is a Python module for writing files in the Excel 2007+ XLSX
    file format."""

    pypi = "XlsxWriter/XlsxWriter-1.0.2.tar.gz"

    license("BSD-2-Clause")

    version(
        "3.1.7",
        sha256="8c730c4beb468696c4160aa1d6d168fb4c1a20dd972b212cd8cc1e74ddeab1b6",
        url="https://pypi.org/packages/51/ba/f6982db11e17b43da310a2169dcfbda166e8c509d8358ec8310219ca9732/XlsxWriter-3.1.7-py3-none-any.whl",
    )
    version(
        "3.0.3",
        sha256="df0aefe5137478d206847eccf9f114715e42aaea077e6a48d0e8a2152e983010",
        url="https://pypi.org/packages/ef/95/30f6ee57f10232e2055a85c3e4c8db7d38ab5f1349b6cdced85cb8acd5e6/XlsxWriter-3.0.3-py3-none-any.whl",
    )
    version(
        "1.4.3",
        sha256="1a7fac99687020e76aa7dd0d7de4b9b576547ed748e5cd91a99d52a6df54ca16",
        url="https://pypi.org/packages/2c/ce/74fd8d638a5b82ea0c6f08a5978f741c2655a38c3d6e82f73a0f084377e6/XlsxWriter-1.4.3-py2.py3-none-any.whl",
    )
    version(
        "1.2.2",
        sha256="00e9c337589ec67a69f1220f47409146ab1affd8eb1e8eaad23f35685bd23e47",
        url="https://pypi.org/packages/25/88/a38f35b00ce4dd166a20e1a0a25e438e19e332e680df52af4aeac0df0f03/XlsxWriter-1.2.2-py2.py3-none-any.whl",
    )
    version(
        "1.0.2",
        sha256="279220b1c58cef2d35b8fd99030945a740a4fde65c0c8598b34177f7e2cd8ffc",
        url="https://pypi.org/packages/c7/86/748cb5f6ef5ff2d95a7f189ef1c5124f9badc1d1293dbc214c128595e57e/XlsxWriter-1.0.2-py2.py3-none-any.whl",
    )
