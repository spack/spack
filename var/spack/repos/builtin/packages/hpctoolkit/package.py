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
    """HPCToolkit is an integrated suite of tools for measurement and analysis
    of program performance on computers ranging from multicore desktop systems
    to the nation's largest supercomputers. By using statistical sampling of
    timers and hardware performance counters, HPCToolkit collects accurate
    measurements of a program's work, resource consumption, and inefficiency
    and attributes them to the full calling context in which they occur."""

    homepage = "http://hpctoolkit.org"

    # Note: No precise release tags/branches provided
    version('5.4', git='https://github.com/HPCToolkit/hpctoolkit.git',
            commit='d9ca2112762e5a06ea31b5295d793e4a83272d19')

    variant('mpi', default=True, description='Enable MPI supoort')
    variant('papi', default=True, description='Enable PAPI counter support')

    depends_on('hpctoolkit-externals')
    depends_on('papi', when='+papi')
    depends_on('mpi', when='+mpi')

    def install(self, spec, prefix):

        options = ['CC=%s' % self.compiler.cc,
                   'CXX=%s' % self.compiler.cxx,
                   '--with-externals=%s' % spec['hpctoolkit-externals'].prefix]

        if '+mpi' in spec:
            options.extend(['MPICXX=%s' % spec['mpi'].mpicxx])

        if '+papi' in spec:
            options.extend(['--with-papi=%s' % spec['papi'].prefix])

        # TODO: BG-Q configure option
        with working_dir('spack-build', create=True):
            configure = Executable('../configure')
            configure('--prefix=%s' % prefix, *options)
            make('install')
