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
import os


class PyBasemap(PythonPackage):
    """The matplotlib basemap toolkit is a library for plotting
    2D data on maps in Python."""

    homepage = "http://matplotlib.org/basemap/"
    url      = "https://downloads.sourceforge.net/project/matplotlib/matplotlib-toolkits/basemap-1.0.7/basemap-1.0.7.tar.gz"

    version('1.0.7', '48c0557ced9e2c6e440b28b3caff2de8')

    depends_on('py-setuptools', type='build')
    depends_on('py-numpy', type=('build', 'run'))
    depends_on('py-matplotlib', type=('build', 'run'))
    depends_on('pil', type=('build', 'run'))
    depends_on('geos')

    def setup_environment(self, spack_env, run_env):
        spack_env.set('GEOS_DIR', self.spec['geos'].prefix)

    @run_after('install')
    def post_install_patch(self):
        spec = self.spec
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
            path_m = find_package_dir(
                spec['py-matplotlib'].prefix, 'mpl_toolkits')
            path_b = find_package_dir(spec.prefix, 'mpl_toolkits')
            link_dir(path_m, path_b)


def find_package_dir(spack_package_root, name):

    """Finds directory with a specific name, somewhere inside a Spack
    package.

    spack_package_root:
        Root directory to start searching
    oldname:
        Original name of package (not fully qualified, just the leaf)
    newname:
        What to rename it to

    """
    for root, dirs, files in os.walk(spack_package_root):
        path = os.path.join(root, name)

        # Make sure it's a directory
        if not os.path.isdir(path):
            continue

        # Make sure it's really a package
        if not os.path.exists(os.path.join(path, '__init__.py')):
            continue

        return path

    return None


def link_dir(src_root, dest_root, link=os.symlink):
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
