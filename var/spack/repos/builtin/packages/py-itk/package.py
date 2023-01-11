# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import sys

import archspec

from spack.package import *


class PyItk(PythonPackage):
    """ITK is an open-source toolkit for multidimensional image analysis"""

    homepage = "https://itk.org/"

    if sys.platform == "darwin":
        # version 5.1.1
        version(
            "5.1.1-cp37",
            url="https://pypi.io/packages/cp35/i/itk/itk-5.1.1-cp37-cp37m-macosx_10_9_x86_64.whl",
            sha256="f112515483a073fae96d5cfce4eb9f95cbf57a145bbd196b2369a3194e27febf",
            expand=False,
        )
        version(
            "5.1.1-cp38",
            url="https://pypi.io/packages/cp35/i/itk/itk-5.1.1-cp38-cp38-macosx_10_9_x86_64.whl",
            sha256="94b09ab9dd59ceaecc456ede2b719a44b8f0d54d92409eede372c6004395ae7b",
            expand=False,
        )
        # version 5.1.2
        version(
            "5.1.2-cp37",
            url="https://pypi.io/packages/cp37/i/itk/itk-5.1.2-cp37-cp37m-macosx_10_9_x86_64.whl",
            sha256="0b494485d05306240eaa5ab1a5e00895fcce8fe684c632c02a2373f36d123902",
            expand=False,
        )
        version(
            "5.1.2-cp38",
            url="https://pypi.io/packages/cp38/i/itk/itk-5.1.2-cp38-cp38-macosx_10_9_x86_64.whl",
            sha256="e8dec75b4452bd2ee65beb4901b245fc3a2a2ccc46dfa008ae0b5b757718d458",
            expand=False,
        )
        version(
            "5.1.2-cp39",
            url="https://pypi.io/packages/cp39/i/itk/itk-5.1.2-cp39-cp39-macosx_10_9_x86_64.whl",
            sha256="e8dec75b4452bd2ee65beb4901b245fc3a2a2ccc46dfa008ae0b5b757718d458",
            expand=False,
        )
    elif sys.platform.startswith("linux"):
        # version 5.1.1
        version(
            "5.1.1-cp37",
            url="https://pypi.io/packages/cp37/i/itk/itk-5.1.1-cp37-cp37m-manylinux1_x86_64.whl",
            sha256="7c313d2e3a3e37b8e78d0b2d70be2d478c87fde6f27912c714c855a05584b8ee",
            expand=False,
        )
        version(
            "5.1.1-cp38",
            url="https://pypi.io/packages/cp38/i/itk/itk-5.1.1-cp38-cp38-manylinux1_x86_64.whl",
            sha256="14cd6c3a25f0d69f45eda74b006eceeaf8e2b2fcbe7c343e49683edf97e0fb14",
            expand=False,
        )
        # version 5.1.2
        version(
            "5.1.2-cp37",
            url="https://pypi.io/packages/cp37/i/itk/itk-5.1.2-cp37-cp37m-manylinux1_x86_64.whl",
            sha256="064d9cfdd9547ae3ed850c35b989e0141c4bd434672bc2dd124248aab7bdf09a",
            expand=False,
        )
        version(
            "5.1.2-cp38",
            url="https://pypi.io/packages/cp38/i/itk/itk-5.1.2-cp38-cp38-manylinux1_x86_64.whl",
            sha256="fe9225ac353116f4000c0a3440bf151200beb4a65deec5b2e626edda5b498f16",
            expand=False,
        )
        version(
            "5.1.2-cp39",
            url="https://pypi.io/packages/cp39/i/itk/itk-5.1.2-cp39-cp39-manylinux1_x86_64.whl",
            sha256="5781b74410b7189a825c89d370411595e5e3d5dbb480201907f751f26698df83",
            expand=False,
        )

    depends_on("python@3.7.0:3.7", when="@5.1.1-cp37,5.1.2-cp37", type=("build", "run"))
    depends_on("python@3.8.0:3.8", when="@5.1.1-cp38,5.1.2-cp38", type=("build", "run"))
    depends_on("python@3.9.0:3.9", when="@5.1.2-cp39", type=("build", "run"))
    depends_on("py-setuptools", type="run")

    for t in set(
        [str(x.family) for x in archspec.cpu.TARGETS.values() if str(x.family) != "x86_64"]
    ):
        conflicts("target={0}:".format(t), msg="py-itk is available for x86_64 only")
