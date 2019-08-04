# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: MIT
#
# ----------------------------------------------------------------------------
#
#     spack install py-google-cloud
#
# You can edit this file again by typing:
#
#     spack edit py-google-cloud
#
# See the Spack documentation for more information on packaging.
# ----------------------------------------------------------------------------

from spack import *


class PyGoogleCloud(PythonPackage):
    """This library is not meant to stand-alone. Instead it defines common helpers used by all Google API clients."""

    homepage = "https://github.com/googleapis/google-cloud-python"
    url      = "https://github.com/googleapis/google-cloud-python/archive/api_core-1.4.1.tar.gz"

    version('1.14.0', 'f62c8249485538751858dd41bd3f2e88')

    # Build dependencies
    depends_on('py-pkgconfig', type='build')
    depends_on('py-setuptools', type='build')
    depends_on('py-protobuf', type=('build', 'run'))
    depends_on('py-google-auth', type=('build', 'run'))
    depends_on('py-google-resumable-media-python')
    depends_on('py-six', type=('build', 'run'))

    phases = ['install']


    def install(self, spec, prefix):
        import subprocess
        import os
        basedir = os.getcwd()
        
        # api_core
        os.chdir('api_core')
        cmd = '{0} setup.py install --prefix={1} --single-version-externally-managed --root=/'.format(spec['python'].command.path, prefix)
        subprocess.call(cmd, shell=True)
        os.chdir(basedir)
        
        # bigquery
        os.chdir('bigquery')
        cmd = '{0} setup.py install --prefix={1} --single-version-externally-managed --root=/'.format(spec['python'].command.path, prefix)
        subprocess.call(cmd, shell=True)
        os.chdir(basedir)
        
        # bigquery_datatransfer
        os.chdir('bigquery_datatransfer')
        cmd = '{0} setup.py install --prefix={1} --single-version-externally-managed --root=/'.format(spec['python'].command.path, prefix)
        subprocess.call(cmd, shell=True)
        os.chdir(basedir)
        
        # bigtable
        os.chdir('bigtable')
        cmd = '{0} setup.py install --prefix={1} --single-version-externally-managed --root=/'.format(spec['python'].command.path, prefix)
        subprocess.call(cmd, shell=True)
        os.chdir(basedir)
        
        # container
        os.chdir('container')
        cmd = '{0} setup.py install --prefix={1} --single-version-externally-managed --root=/'.format(spec['python'].command.path, prefix)
        subprocess.call(cmd, shell=True)
        os.chdir(basedir)
        
        # core
        os.chdir('core')
        cmd = '{0} setup.py install --prefix={1} --single-version-externally-managed --root=/'.format(spec['python'].command.path, prefix)
        subprocess.call(cmd, shell=True)
        os.chdir(basedir)
        
        # storage
        os.chdir('storage')
        cmd = '{0} setup.py install --prefix={1} --single-version-externally-managed --root=/'.format(spec['python'].command.path, prefix)
        subprocess.call(cmd, shell=True)
        os.chdir(basedir)


