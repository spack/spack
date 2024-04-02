# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PySubwordNmt(PythonPackage):
    """This repository contains preprocessing scripts to segment text into
    subword units."""

    # pypi only has the whl file.
    homepage = "https://github.com/joeynmt/joeynmt"
    url = "https://github.com/rsennrich/subword-nmt/archive/refs/tags/v0.3.7.zip"

    license("MIT")

    version(
        "0.3.7",
        sha256="a2d92eed5dea55f2b1c9b21225a57b3ae7009ce8a1fa4d2e3f01ab11435c28c9",
        url="https://pypi.org/packages/74/60/6600a7bc09e7ab38bc53a48a20d8cae49b837f93f5842a41fe513a694912/subword_nmt-0.3.7-py2.py3-none-any.whl",
    )
