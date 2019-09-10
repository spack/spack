# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyConfigargparse(PythonPackage):
    """A drop-in replacement for argparse that allows options to also be
    set via config files and/or environment variables."""

    homepage = "https://github.com/bw2/ConfigArgParse"
    url      = "https://pypi.io/packages/source/C/ConfigArgParse/ConfigArgParse-3.11.2.tar.gz"

    version('0.14.0', '2e2efe2be3f90577aca9415e32cb629aa2ecd92078adbe27b53a03e53ff12e91')

    depends_on('py-setuptools', type=('build', 'run'))
