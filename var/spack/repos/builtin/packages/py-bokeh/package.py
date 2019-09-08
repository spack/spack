# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyBokeh(PythonPackage):
    """Statistical and novel interactive HTML plots for Python"""

    homepage = "http://github.com/bokeh/bokeh"
    url      = "https://pypi.io/packages/source/b/bokeh/bokeh-0.12.2.tar.gz"

    version('1.3.4', 'e2d97bed5b199a10686486001fed5c854e4c04ebe28859923f27c52b93904754')
    version('0.12.2', '2d1621bffe6e2ab9d42efbf733861c4f')

    depends_on('python@2.6:',             type=('build', 'run'), when='@0.12.2')
    depends_on('python@2.7:',             type=('build', 'run'), when='@1.3.4:')
    depends_on('py-requests@1.2.3:',      type=('build', 'run'), when='@0.12.2')
    depends_on('py-pillow@4.0:',          type=('build', 'run'), when='@1.3.4:')
    depends_on('py-packaging@16.8:',      type=('build', 'run'), when='@1.3.4:')
    depends_on('py-six@1.5.2:',           type=('build', 'run'))
    depends_on('py-pyyaml@3.10:',         type=('build', 'run'))
    depends_on('py-python-dateutil@2.1:', type=('build', 'run'))
    depends_on('py-jinja2@2.7:',          type=('build', 'run'))
    depends_on('py-numpy@1.7.1:',         type=('build', 'run'))
    depends_on('py-tornado@4.3:',         type=('build', 'run'))
    depends_on('py-futures@3.0.3:',       type=('build', 'run'), when='^python@2.7:2.8')
