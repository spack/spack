##############################################################################
# Copyright (c) 2013-2016, Lawrence Livermore National Security, LLC.
# Produced at the Lawrence Livermore National Laboratory.
#
# This file is part of Spack.
# Created by Todd Gamblin, tgamblin@llnl.gov, All rights reserved.
# LLNL-CODE-647188
#
# For details, see https://github.com/llnl/spack
# Please also see the LICENSE file for our notice and the LGPL.
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License (as
# published by the Free Software Foundation) version 2.1, February 1999.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the IMPLIED WARRANTY OF
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the terms and
# conditions of the GNU Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public
# License along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA 02111-1307 USA
##############################################################################
from spack import *


class PySpyder(PythonPackage):
    """Scientific PYthon Development EnviRonment"""

    homepage = "https://github.com/spyder-ide/spyder"
    url      = "https://pypi.io/packages/source/s/spyder/spyder-3.1.3.tar.gz"

    version('3.1.3', '4b9b7c8c3e6dc00001e6e98473473c36')
    version('2.3.9', 'dd01e07a77123c128ff79ba57b97c1d7')

    depends_on('py-setuptools',       type='build')
    depends_on('py-rope@0.9.4:',      type=('build', 'run'), when='^python@:3')
    # depends_on('py-rope_py3k',    type=('build', 'run'), when='^python@3:')
    depends_on('py-jedi@0.9.0',       type=('build', 'run'))
    # otherwise collision with py-flake8
    depends_on('py-pyflakes@1.2.3',   type=('build', 'run'))
    depends_on('py-pygments@2.0:',    type=('build', 'run'))
    depends_on('py-qtconsole@4.2.0:', type=('build', 'run'))
    depends_on('py-nbconvert',        type=('build', 'run'))
    depends_on('py-sphinx',           type=('build', 'run'))
    depends_on('py-pycodestyle',      type=('build', 'run'))
    depends_on('py-pylint',           type=('build', 'run'))
    depends_on('py-psutil',           type=('build', 'run'))
    depends_on('py-qtawesome@0.4.1:', type=('build', 'run'))
    depends_on('py-qtpy@1.1.0:',      type=('build', 'run'))
    depends_on('py-zmq',              type=('build', 'run'))
    depends_on('py-chardet@2:',       type=('build', 'run'))
    depends_on('py-pickleshare',      type=('build', 'run'))
    depends_on('py-numpydoc',         type=('build', 'run'))
