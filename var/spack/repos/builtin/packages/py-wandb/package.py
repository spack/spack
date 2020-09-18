# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyWandb(PythonPackage):
    """A tool for visualizing and tracking your machine
    learning experiments."""

    homepage = "https://github.com/wandb/"
    url      = "https://github.com/wandb/client/archive/v0.10.1.tar.gz"

    version('0.10.1', sha256='abd334cd1460ac1f6e5aa959d3e04c46cd246f96cfc3323fc0572916760d32ab')

    depends_on('py-setuptools', type='build')
