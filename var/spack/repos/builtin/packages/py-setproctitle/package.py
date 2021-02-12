# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PySetproctitle(PythonPackage):
    """The setproctitle module allows a process to change its title (as
    displayed by system tools such as ps and top)."""

    homepage = "https://github.com/dvarrazzo/py-setproctitle"
    pypi = "setproctitle/setproctitle-1.1.10.tar.gz"

    version('1.2.2', sha256='7dfb472c8852403d34007e01d6e3c68c57eb66433fb8a5c77b13b89a160d97df')
    version('1.2.1', sha256='5f0eecb27815e31799a69eb6a06b4d375d38887d079d410565b0be82da65c950')
    version('1.2',   sha256='9b4e48722dd96cbd66d5bf2eab930fff8546cd551dd8d774c8a319448bd381a6')
    version('1.1.10', sha256='6283b7a58477dd8478fbb9e76defb37968ee4ba47b05ec1c053cb39638bd7398')

    depends_on('py-setuptools', type='build')
