# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

# ----------------------------------------------------------------------------
# If you submit this package back to Spack as a pull request,
# please first remove this boilerplate and all FIXME comments.
#
# This is a template package file for Spack.  We've put "FIXME"
# next to all the things you'll want to change. Once you've handled
# them, you can save this file and test your package like this:
#
#     spack install eodatadown
#
# You can edit this file again by typing:
#
#     spack edit eodatadown
#
# See the Spack documentation for more information on packaging.
# ----------------------------------------------------------------------------

from spack import *


class PyEodatadown(PythonPackage):
    """A tool for automating Earth Observation Data Downloading and ARD Production."""

    homepage = "https://www.remotesensing.info/eodatadown"
    url      = "https://bitbucket.org/petebunting/eodatadown/downloads/EODataDown-0.13.0.tar.gz"

    maintainers = ['petebunting']

    version('0.13.0', sha256='75854c99a259c4ddcf6cdbff6aab946d2e1c69bc4ba12a4ed256270af65947f9')

    # Add dependencies if required.
    depends_on('py-setuptools',    type='build')
    depends_on('python',           type=('build', 'run'))
    depends_on('rsgislib',         type=('build', 'run'))
    depends_on('py-arcsi',         type=('build', 'run'))
    depends_on('py-google-cloud',  type=('build', 'run'))
    depends_on('py-planet',        type=('build', 'run'))
    depends_on('py-sqlalchemy',    type=('build', 'run'))
    depends_on('py-pycurl',        type=('build', 'run'))
    depends_on('py-psycopg2',      type=('build', 'run'))
    depends_on('py-pyyaml',        type=('build', 'run'))
    depends_on('wget',             type=('build', 'run'))
    depends_on('postgresql',       type=('build', 'run'))


    def install(self, spec, prefix):
        import subprocess
        cmd = '{0} setup.py install --prefix={1}'.format(spec['python'].command.path, prefix)
        subprocess.call(cmd, shell=True)

