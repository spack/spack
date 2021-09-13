# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyTfSlim(PythonPackage):
    """TF-Slim is a lightweight library for defining, training
    and evaluating complex models in TensorFlow. Components of
    tf-slim can be freely mixed with native tensorflow, as well
    as other frameworks."""

    homepage = "https://github.com/google-research/tf-slim"
    url      = "https://github.com/google-research/tf-slim/archive/refs/tags/v1.1.0.tar.gz"

    version('1.1.0', sha256='964cde4b7728a408dcd5c841ab6b93d95137ab4b60db28b10400f86286bfeb8b')

    depends_on('py-setuptools', type='build')
    depends_on('py-absl-py@0.2.2:', type='build')
    depends_on('py-six', type='run')
    depends_on('py-wrapt', type='run')
    depends_on('py-gast', type='run')
    depends_on('py-termcolor', type='run')
    depends_on('flatbuffers', type='run')
