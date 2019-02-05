# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyXdot(PythonPackage):
    """xdot.py is an interactive viewer for graphs written in Graphviz's
    dot language."""

    homepage = "https://github.com/jrfonseca/xdot.py"
    url      = "https://github.com/jrfonseca/xdot.py/archive/0.9.tar.gz"
    git      = "https://github.com/jrfonseca/xdot.py.git"

    version('master', branch="master")
    version('1.0', '4e60c42d009a8802db6c1b4dab519863')
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
            join_path(spec['atk'].prefix.lib, 'girepository-1.0'),
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
                             join_path(spec['atk'].prefix.lib,
                                       'girepository-1.0'))
        run_env.prepend_path('GI_TYPELIB_PATH',
                             join_path(spec['gdk-pixbuf'].prefix.lib,
                                       'girepository-1.0'))
        run_env.prepend_path('GI_TYPELIB_PATH',
                             join_path(spec['gtkplus'].prefix.lib,
                                       'girepository-1.0'))
