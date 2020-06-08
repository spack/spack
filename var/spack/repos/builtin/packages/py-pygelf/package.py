# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyPygelf(PythonPackage):
    """Python logging handlers with GELF (Graylog Extended Log Format) support."""

    homepage = "https://github.com/keeprocking/pygelf"
    url      = "https://files.pythonhosted.org/packages/5e/4f/a6224902db19be061ffb090a247014c4716d45e5c97ae4d143321e818092/pygelf-0.3.6.tar.gz"

    # notify when the package is updated.
    maintainers = ['victorusu', 'vkarak']

    version('0.3.6', sha256='3e5bc59e3b5a754556a76ff2c69fcf2003218ad7b5ff8417482fa1f6a7eba5f9')

    depends_on('python@3:', type=('run'))
    depends_on('py-setuptools', type=('build', 'run'))

