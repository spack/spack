from spack import *
import subprocess
from glob import glob

class Wrf(Package):
    """Description"""

    homepage = "http://www.example.com"
    url      = "http://www2.mmm.ucar.edu/wrf/src/WRFV3.6.1.TAR.gz"

    version('3.6.1')

    depends_on('netcdf')
    depends_on('netcdf-fortran')
    depends_on('jasper')

    def install(self, spec, prefix):
        process=subprocess.Popen(['./configure'], stdin=subprocess.PIPE)
        process.communicate(input='32\n')
        subprocess.call(['./compile', 'all_wrfvar'])
        subprocess.call(['cp', '-r'] + glob('*') + [prefix])
