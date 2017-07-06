##############################################################################
# Copyright (c) 2013-2016, Lawrence Livermore National Security, LLC.
# Produced at the Lawrence Livermore National Laboratory.
#
# This file is part of Spack.
# Created by Todd Gamblin, tgamblin@llnl.gov, All rights reserved.
# LLNL-CODE-647188
#
# For details, see https://github.com/llnl/spack
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
from spack import *
from spack.package import PackageBase


class PyEntrypoints(PythonPackage):
    """Discover and load entry points from installed packages."""

    homepage = "https://pypi.python.org/pypi/entrypoints"
    url      = "https://pypi.python.org/packages/f8/ad/0e77a853c745a15981ab51fa9a0cb4eca7a7a007b4c1970106ee6ba01e0c/entrypoints-0.2.2-py2.py3-none-any.whl"

    import_modules = ['entrypoints']

    version('0.2.2', '73bd7ce92c19b25dc5a20aff41be996a', expand=False)

    depends_on('python@2.7:', type=('build', 'run'))

    depends_on('py-pip', type='build')
    depends_on('py-configparser', when='^python@:2.8', type=('build', 'run'))

    phases = ['install']

    def install(self, spec, prefix):
        pip = which('pip')
        pip('install', self.stage.archive_file, '--prefix={0}'.format(prefix))

    run_after('install')(PackageBase._run_default_install_time_test_callbacks)

    # Check that self.prefix is there after installation
    run_after('install')(PackageBase.sanity_check_prefix)
