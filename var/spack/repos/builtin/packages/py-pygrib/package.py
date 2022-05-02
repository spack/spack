# Copyright 2010 Jeffrey Whitaker
# 
# Permission is hereby granted, free of charge, to any person obtaining a copy of 
# this software and associated documentation files (the "Software"), to deal in the 
# Software without restriction, including without limitation the rights to use, 
# copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the 
# Software, and to permit persons to whom the Software is furnished to do so, 
# subject to the following conditions:
# 
# The above copyright notice and this permission notice shall be included in all 
# copies or substantial portions of the Software.
# 
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR 
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS 
# FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR 
# COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN 
# AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION 
# WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

from spack import *


class PyPygrib(PythonPackage):
    """A high-level interface to the ECWMF ECCODES C library for reading GRIB files."""

    homepage = "https://github.com/jswhit/pygrib"
    pypi = "pygrib/pygrib-2.1.4.tar.gz"

    version('2.1.4', sha256='951a409eb3233dd95839dd77c0dbe4d8cbed8f21a4015b1047dec9edec65f545')

    depends_on('eccodes', type=('build', 'run'))

    depends_on('py-setuptools', type=('build', 'run'))
    depends_on('py-cython', type=('build', 'run'))
    depends_on('py-numpy', type=('build', 'run'))
    depends_on('py-proj', type=('run'))
    
    #depends_on('python@2.6:2.8,3.2:', type=('build', 'run'), when='@0.9.0')
    #depends_on('python@2.6:2.8,3.3:', type=('build', 'run'), when='@0.10.0')
    #depends_on('python@2.7:2.8,3.4:', type=('build', 'run'), when='@0.13.3')
    #depends_on('python@2.7:2.8,3.5:', type=('build', 'run'), when='@0.17.2')
    #depends_on('python@3.6:', type=('build', 'run'), when='@0.18.0')



