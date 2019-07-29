##############################################################################
# Copyright (c) 2013-2018, Lawrence Livermore National Security, LLC.
# Produced at the Lawrence Livermore National Laboratory.
#
# This file is part of Spack.
# Created by Todd Gamblin, tgamblin@llnl.gov, All rights reserved.
# LLNL-CODE-647188
#
# For details, see https://github.com/spack/spack
# Please also see the NOTICE and LICENSE files for our notice and the LGPL.
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
#
# This is a template package file for Spack.  We've put "FIXME"
# next to all the things you'll want to change. Once you've handled
# them, you can save this file and test your package like this:
#
#     spack install py-python-fmask
#
# You can edit this file again by typing:
#
#     spack edit py-python-fmask
#
# See the Spack documentation for more information on packaging.
# If you submit this package back to Spack as a pull request,
# please first remove this boilerplate and all FIXME comments.
#
from spack import *


class PyPythonFmask(PythonPackage):
    """A set of command line utilities and Python modules that implement 
       the FMASK algorithm for Landsat and Sentinel-2"""

    homepage = "http://pythonfmask.org"
    url      = "https://bitbucket.org/chchrsc/python-fmask/downloads/python-fmask-0.4.5.tar.gz"

    version('0.4.5', 'a0223906b8d1532129072fd71c645870')
    version('0.3.0', 'a8395883f6a0efe4126fae3eac327604')
    version('0.2.1', '525ddba46e1ce75f93915e828ed6de54')
    version('0.2',   '34c1bf5850b51ff7fea15c3d252a067d')

    # Add dependencies if required.
    depends_on('py-setuptools', type='build')
    depends_on('py-rios', type=('build', 'run'))
    depends_on('py-numpy', type=('build', 'run'))
    depends_on('py-scipy', type=('build', 'run'))
    depends_on('python', type=('build', 'run'))
    
    def install(self, spec, prefix):
        import subprocess
        cmd = '{0} setup.py install --prefix={1}'.format(spec['python'].command.path, prefix)
        subprocess.call(cmd, shell=True)


