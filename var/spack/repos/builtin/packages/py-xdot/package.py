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
from spack import *


class PyXdot(PythonPackage):
    """xdot.py is an interactive viewer for graphs written in Graphviz's
    dot language."""

    homepage = "https://github.com/jrfonseca/xdot.py"
    url      = "https://github.com/jrfonseca/xdot.py/archive/0.9.tar.gz"
    git      = "https://github.com/jrfonseca/xdot.py.git"

    version('master', branch="master")
    version('0.9.1', commit="0fa629166989576b05d509c7ef0329c0f7655190")
    version('0.9', '19c78311d73b0f9ea059a6febf42eeea')

    # setuptools is required at runtime to avoid:
    # No module named 'pkg_resources'
    depends_on('py-setuptools', type=('build', 'run'))
    depends_on('python@3:', type=('build', 'run'))
    depends_on('py-pygobject', type=('build', 'run'))
    depends_on('py-pycairo', type=('build', 'run'))
    depends_on('pango', type=('build', 'run'))
    depends_on('atk', type=('build', 'run'))
    depends_on('gdk-pixbuf', type=('build', 'run'))
    depends_on('gtkplus', type=('build', 'run'))

    @run_after('install')
    def post_install(self):
        spec = self.spec
        repo_paths = '%s:%s:%s:%s' % (
            join_path(spec['pango'].prefix.lib, 'girepository-1.0'),
            join_path(spec['atk'].prefix.lib64, 'girepository-1.0'),
            join_path(spec['gdk-pixbuf'].prefix.lib, 'girepository-1.0'),
            join_path(spec['gtkplus'].prefix.lib, 'girepository-1.0'))
        dst = join_path(spec.prefix, spec['python'].package.site_packages_dir,
                        'xdot/__init__.py')
        filter_file("import sys",
                    "import sys\nimport os\nos.environ['GI_TYPELIB_PATH']" +
                    " = '%s'" % repo_paths, dst)
        # regenerate the byte-compiled __init__.py
        python3 = spec['python'].command
        python3('-m', 'compileall', dst)

    def setup_environment(self, spack_env, run_env):
        spec = self.spec
        run_env.prepend_path('GI_TYPELIB_PATH',
                             join_path(spec['pango'].prefix.lib,
                                       'girepository-1.0'))
        run_env.prepend_path('GI_TYPELIB_PATH',
                             join_path(spec['atk'].prefix.lib64,
                                       'girepository-1.0'))
        run_env.prepend_path('GI_TYPELIB_PATH',
                             join_path(spec['gdk-pixbuf'].prefix.lib,
                                       'girepository-1.0'))
        run_env.prepend_path('GI_TYPELIB_PATH',
                             join_path(spec['gtkplus'].prefix.lib,
                                       'girepository-1.0'))
