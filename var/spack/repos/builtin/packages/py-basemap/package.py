# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *
import os

def my_find_package_dir(spack_package_root, name):

    """Finds directory with a specific name, somewhere inside a Spack
    package.
    spack_package_root:
        Root directory to start searching
    oldname:
        Original name of package (not fully qualified, just the leaf)
    newname:
        What to rename it to
    """
    print('find_package_dir', spack_package_root, name)
    for root, dirs, files in os.walk(spack_package_root):
        path = os.path.join(root, name)

        # Make sure it's a directory
        if not os.path.isdir(path):
            continue

#        # Make sure it's really a package
#        if not os.path.exists(os.path.join(path, '__init__.py')):
#            continue

        print('      --> returns {}'.format(path))
        return path

    print('     --> returns None')
    return None


def my_link_dir(src_root, dest_root, link=os.symlink):
    """Link all files in src_root into directory dest_root"""

    for src_path, dirnames, filenames in os.walk(src_root):
        if not filenames:
            continue        # avoid explicitly making empty dirs

        # Avoid internal Python stuff
        src_leaf = os.path.split(src_path)[1]
        if src_leaf.startswith('__'):
            continue

        # Make sure the destination directory exists
        dest_path = os.path.join(dest_root, src_path[len(src_root) + 1:])
        try:
            os.makedirs(dest_path)
        except:
            pass

        # Link all files from src to dest directory
        for fname in filenames:
            src = os.path.join(src_path, fname)
            dst = os.path.join(dest_path, fname)
            if not os.path.exists(dst):
                link(src, dst)


class PyBasemap(PythonPackage):
    """The matplotlib basemap toolkit is a library for plotting
    2D data on maps in Python."""

    homepage = "http://matplotlib.org/basemap/"
    url      = "https://downloads.sourceforge.net/project/matplotlib/matplotlib-toolkits/basemap-1.0.7/basemap-1.0.7.tar.gz"

    version('1.0.7', '48c0557ced9e2c6e440b28b3caff2de8')

    # Per Github issue #3813, setuptools is required at runtime in order
    # to make mpl_toolkits a namespace package that can span multiple
    # directories (i.e., matplotlib and basemap)
    depends_on('py-setuptools', type=('run'))
    depends_on('py-numpy', type=('build', 'run'))
    depends_on('py-matplotlib', type=('build', 'run'))
    depends_on('pil', type=('build', 'run'))
    depends_on('geos')

    def setup_environment(self, spack_env, run_env):
        spack_env.set('GEOS_DIR', self.spec['geos'].prefix)

    def install(self, spec, prefix):
        """Install everything from build directory."""
        args = self.install_args(spec, prefix)

        self.setup_py('install', *args)

        # We are not sure if this fix is needed before Python 3.5.2.
        # If it is needed, this test should be changed.
        # See: https://github.com/LLNL/spack/pull/1964
        if spec['python'].version >= Version('3.5.2'):
            # Use symlinks to join the two mpl_toolkits/ directories into
            # one, inside of basemap.  This is because Basemap tries to
            # "add to" an existing package in Matplotlib, which is only
            # legal Python for "Implicit Namespace Packages":
            #     https://www.python.org/dev/peps/pep-0420/
            #     https://github.com/Homebrew/homebrew-python/issues/112
            # In practice, Python will see only the basemap version of
            # mpl_toolkits
            path_m = my_find_package_dir(
                spec['py-matplotlib'].prefix, 'mpl_toolkits')
            path_b = my_find_package_dir(spec.prefix, 'mpl_toolkits')
            print('path_m',path_m,type(path_m))
            print('path_b',path_b,type(path_b))
            my_link_dir(path_m, path_b)


