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


class HpctoolkitExternals(Package):
    """HPCToolkit performance analysis tool has many prerequisites and
    HpctoolkitExternals package provides all these prerequisites."""

    homepage = "http://hpctoolkit.org"

    # Note: No precise release tags/branches provided
    version('5.4',
            git='https://github.com/HPCToolkit/hpctoolkit-externals.git',
            commit='3d2953623357bb06e9a4b51eca90a4b039c2710e')

    parallel = False

    def install(self, spec, prefix):

        options = ['CC=%s' % self.compiler.cc,
                   'CXX=%s' % self.compiler.cxx]

        with working_dir('spack-build', create=True):
            configure = Executable('../configure')
            configure('--prefix=%s' % prefix, *options)
            make('install')
