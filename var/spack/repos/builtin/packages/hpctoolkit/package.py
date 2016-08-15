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


class Hpctoolkit(Package):

    """
    HPCToolkit is an integrated suite of tools for measurement and analysis of
    program performance on computers ranging from multicore desktop systems to
    the nation's largest supercomputers. By using statistical sampling of timers
    and hardware performance counters, HPCToolkit collects accurate measurements
    of a program's work, resource consumption, and inefficiency and attributes
    them to the full calling context in which they occur.
    """

    homepage = "http://hpctoolkit.org"
    url      = "https://github.com/HPCToolkit/hpctoolkit.git"

    version('develop', git='https://github.com/HPCToolkit/hpctoolkit.git')

    depends_on("hpctoolkit-externals")
    depends_on("papi")
    depends_on("mpi")

    def install(self, spec, prefix):

        mkdirp('build')
        cd('build')

        config_hpctoolkit = Executable('../configure')
        config_hpctoolkit(
            "--prefix=%s" % prefix,
            "--with-externals=%s" % spec['hpctoolkit-externals'].prefix,
            "--with-papi=%s" % spec['papi'].prefix,
            'CC=cc',
            'CXX=c++',
            'CXX={0}'.format(spec['mpi'].mpicxx))

        make()
        make('install')
