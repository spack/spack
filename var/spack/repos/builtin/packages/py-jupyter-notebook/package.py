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


class PyJupyterNotebook(PythonPackage):
    """Jupyter Interactive Notebook"""

    homepage = "https://github.com/jupyter/notebook"
    url      = "https://github.com/jupyter/notebook/archive/4.2.3.tar.gz"

    version('4.2.3', '5c6b0b1303adacd8972c4db21eda3e98')
    version('4.2.2', '7f9717ae4fed930d187a44c0707b6379')
    version('4.2.1', '4286f1eaf608257bd69cad4042c7c2fe')
    version('4.2.0', '136be6b72fe9db7f0269dc7fa5652a62')
    version('4.1.0', '763ab54b3fc69f6225b9659b6994e756')
    version('4.0.6', 'd70d8a6d01893f4b64df9edbc0e13b52')
    version('4.0.5', '2681a70e4c62aafe7ce69f1da5799ac8')
    version('4.0.4', 'ab72f28f6af8107d71241a4110e92c05')
    version('4.0.3', '119beea793865ee4b1673a50043ead2a')
    version('4.0.2', '77f371e9a23a840d14d8a60fee7ba1b7')

    variant('terminal', default=False, description="Enable terminal functionality")

    depends_on('py-setuptools', type='build')
    depends_on('python@2.7:2.7.999,3.3:')
    depends_on('npm', type='build')
    depends_on('py-jinja2', type=('build', 'run'))
    depends_on('py-tornado@4:', type=('build', 'run'))
    depends_on('py-ipython-genutils', type=('build', 'run'))
    depends_on('py-traitlets', type=('build', 'run'))
    depends_on('py-jupyter-core', type=('build', 'run'))
    depends_on('py-jupyter-client', type=('build', 'run'))
    depends_on('py-jupyter-console', type=('build', 'run'))
    depends_on('py-nbformat', type=('build', 'run'))
    depends_on('py-nbconvert', type=('build', 'run'))
    depends_on('py-ipykernel', type=('build', 'run'))
    depends_on('py-terminado@0.3.3:', when="+terminal", type=('build', 'run'))
    depends_on('py-ipywidgets', when="+terminal", type=('build', 'run'))
