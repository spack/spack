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

    """
    HPCToolkit has many prerequisites and externals tree is an attempt to deal
    with these prerequisites.  It scans your system to identify which packages
    are available and attempts to build the ones that are missing.
    It contains several external libraries. (Some of these libraries, like libelf and
    libxml2 are commonly found on Linux systems, but not always. Others, like OpenAnalysis
    and SymtabAPI are almost never available. Finally, a few packages, like GNU binutils
    have been heavily patched.) In some cases it may be possible to use versions of these
    packages that are already installed on your system. However, such configurations are
    not supported.
    """

    homepage = "http://hpctoolkit.org"
    url      = "https://github.com/HPCToolkit/hpctoolkit-externals.git"

    version('develop', git='https://github.com/HPCToolkit/hpctoolkit-externals.git')

    depends_on("libelf")
    depends_on("libxml2")

    def install(self, spec, prefix):

        mkdirp('build')
        cd('build')

        config_hpctoolkitext = Executable('../configure')
        config_hpctoolkitext(
            "--prefix=%s" % prefix,
            'CC=cc',
            'CXX=c++')

        make()
        make('install')
