from spack import *
import subprocess
from glob import glob
import fileinput

class Wrf(Package):
    """Description"""

    homepage = "http://www.example.com"
    url      = "http://www2.mmm.ucar.edu/wrf/src/WRFV3.6.1.TAR.gz"

    version('3.6.1')

    depends_on('ben-netcdf')
    depends_on('ben-netcdf-fortran')
    depends_on('jasper')
    depends_on('tcsh')

    def install(self, spec, prefix):
        first = True
        for line in fileinput.input("compile", inplace=True):
            if first:
                first = False
                print "#!%s/csh -f" % spec['tcsh'].prefix.bin,
            else:
                print line,
        fileinput.close()
        process=subprocess.Popen(['./configure'], stdin=subprocess.PIPE)
        process.communicate(input='32\n')
        subprocess.call(['./compile', 'all_wrfvar'])
        subprocess.call(['./compile', 'em_b_wave'])
        subprocess.call(['cp', '-r'] + glob('*') + [prefix])
