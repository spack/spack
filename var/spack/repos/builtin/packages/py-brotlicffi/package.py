# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyBrotlicffi(PythonPackage):
    """BrotliCFFI contains Python CFFI bindings for the reference Brotli
    encoder/decoder."""

    homepage = "https://github.com/python-hyper/brotlicffi"
    pypi = "brotlicffi/brotlicffi-1.0.9.2.tar.gz"

    version("1.0.9.2", sha256="0c248a68129d8fc6a217767406c731e498c3e19a7be05ea0a90c3c86637b7d96")

    depends_on("py-setuptools", type="build")
    depends_on("py-cffi@1.0.0:", type=("build", "run"))

    # TODO: Builds against internal copy of headers, doesn't seem to be a way
    # to use external brotli installation
    # depends_on('brotli')
