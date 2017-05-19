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
import subprocess


class JupyterNotebook(Package):
    """A web application that allows you to create and share documents that
    contain live code, equations, visualizations and explanatory text. Uses
    include: data cleaning and transformation, numerical simulation,
    statistical modeling, machine learning and much more."""

    homepage = "http://jupyter.org/"
    url      = "https://github.com/jupyter/notebook/archive/4.2.1.tar.gz"

    version('4.2.1', '4286f1eaf608257bd69cad4042c7c2fe')
    version('4.2.0', '136be6b72fe9db7f0269dc7fa5652a62')
    version('4.1.0', '763ab54b3fc69f6225b9659b6994e756')
    version('4.0.6', 'd70d8a6d01893f4b64df9edbc0e13b52')

    variant('ipython',         default=True, description='Enable ipython support')
    # variant('ipywidgets',     default=False,  description='Enable with support')  # NOQA: ignore=E501
    # variant('ipyparallel',    default=False,  description='Enable with support')  # NOQA: ignore=E501
    variant('jupyter_console', default=True, description='Enable console support')

    # (Anecdotal) List of sources required to install Jupyer:
    # http://simnotes.github.io/blog/installing-jupyter-on-hdp-2.3.2/

    def cmd_exists(cmd):
        try:
            subprocess.check_output(["which", cmd])
            return True
        except subprocess.CalledProcessError:
            return False

    if (cmd_exists("bower") is False &
       cmd_exists("npm") is False &
       cmd_exists("node") is False):
        depends_on('node-js',   type='build')
        depends_on('npm',       type='build')

    depends_on('python@2.7:2.8,3.3:')
    depends_on('py-setuptools',       type='build')
    depends_on('py-ipython',          when="+ipython")
    # depends_on('py-ipyparallel',      when="+ipyparallel")
    # depends_on('py-ipywidgets',       when="+ipywidgets")
    depends_on('py-jinja2')
    depends_on('py-jsonschema')
    depends_on('py-jupyter_core')
    depends_on('py-jupyter_client')
    depends_on('py-jupyter_console',  when="+jupyter_console")
    depends_on('py-jupyter_nbconvert')
    depends_on('py-jupyter_nbformat')
    depends_on('py-matplotlib')
    depends_on('py-numpy')
    depends_on('py-pandas')
    depends_on('py-pygments')
    depends_on('py-scipy')
    depends_on('py-scikit-learn')
    depends_on('py-tornado')
    depends_on('py-zmq')

    # Unfortunately either bower (preferred?) or npm must be used to install
    # the remaining dependencies. If bower is in path, this is automatically
    # invoked from within the setup script. But as a fall-back npm is installed
    # and will be called if Bower is not present on the system...
    def install(self, spec, prefix):
        setup_py('install', '--prefix={0}'.format(prefix))
