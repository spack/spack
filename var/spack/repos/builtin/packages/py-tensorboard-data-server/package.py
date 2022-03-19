# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyTensorboardDataServer(PythonPackage):
    """Fast data loading for TensorBoard"""

    homepage = "https://github.com/tensorflow/tensorboard/tree/master/tensorboard/data/server"
    url      = "https://pypi.io/packages/py3/t/tensorboard-data-server/tensorboard_data_server-0.6.1-py3-none-any.whl"
    list_url = "https://pypi.org/simple/tensorboard-data-server/"

    version('0.6.1', sha256='809fe9887682d35c1f7d1f54f0f40f98bb1f771b14265b453ca051e2ce58fca7', expand=False)

    depends_on('python@3.6:', type=('build', 'run'))
