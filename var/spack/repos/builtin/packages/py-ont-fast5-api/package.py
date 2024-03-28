# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyOntFast5Api(PythonPackage):
    """This project provides classes and utility functions for working with
    read fast5 files. It provides an abstraction layer between the underlying
    h5py library and the various concepts central to read fast5 files, such as
    "reads", "analyses", "analysis summaries", and "analysis datasets".
    Ideally all interaction with a read fast5 file should be possible via this
    API, without having to directly invoke the h5py library."""

    homepage = "https://github.com/nanoporetech/ont_fast5_api"
    pypi = "ont-fast5-api/ont-fast5-api-0.3.2.tar.gz"

    license("MPL-2.0")

    version(
        "4.1.0",
        sha256="92bf1f12e042db4fdfffbaa757b27f92e049fe922b204ae83ec720a72d20bcd3",
        url="https://pypi.org/packages/60/1b/b67baa5fe047344c17089cbddd25ff181238dd7187d04c5e11aabe47f03b/ont_fast5_api-4.1.0-py3-none-any.whl",
    )
    version(
        "0.3.2",
        sha256="db8d302d215f8c7b82252d9e0f162ef294de1a749a2d27e675615b3d537c03d8",
        url="https://pypi.org/packages/ac/ad/4ccffa38e299d36d0ea1efb6390e37b95a6fe0bee5008db50f01113ef440/ont_fast5_api-0.3.2-py2.py3-none-any.whl",
    )

    with default_args(type="run"):
        depends_on("py-h5py@2.10:", when="@4.0.1:4.1.1")
        depends_on("py-h5py", when="@:0")
        depends_on("py-numpy@1.16.0:", when="@3.2:")
        depends_on("py-numpy@1.8.1:", when="@:1")
        depends_on("py-packaging", when="@3.0.2:")
        depends_on("py-progressbar33", when="@1:")
