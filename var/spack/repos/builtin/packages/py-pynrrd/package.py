# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyPynrrd(PythonPackage):
    """Python library for reading and writing NRRD files into and from numpy arrays"""

    homepage = "https://github.com/mhe/pynrrd"
    url = "https://pypi.io/packages/source/p/pynrrd/pynrrd-0.3.5.tar.gz"

    version('0.3.5', sha256='190bc76e26eebd8cfda5acfdbcecedd062f28e911aebe9399e370396e32c7e8e', preferred=True)

    depends_on('py-numpy', type='run')
