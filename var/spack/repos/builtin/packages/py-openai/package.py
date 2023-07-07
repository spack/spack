# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyOpenai(PythonPackage):
    """The OpenAI Python library provides convenient access to the OpenAI API
    from applications written in the Python language. It includes a pre-defined
    set of classes for API resources that initialize themselves dynamically from
    API responses which makes it compatible with a wide range of versions of the
    OpenAI API."""

    homepage = "https://github.com/openai/openai-python"
    pypi = "openai/openai-0.27.8.tar.gz"

    version("0.27.8", sha256="2483095c7db1eee274cebac79e315a986c4e55207bb4fa7b82d185b3a2ed9536")

    depends_on("py-setuptools", type="build")
