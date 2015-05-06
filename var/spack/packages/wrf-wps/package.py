from spack import *
import subprocess
from glob import glob

class WrfWps(Package):
    """Description"""

 #   homepage = "http://www.example.com"
    url      = "http://www2.mmm.ucar.edu/wrf/src/WPSV3.6.1.TAR.gz"

    version('3.6.1') 
    
    depends_on('netcdf-fortran')
    depends_on('netcdf')
    depends_on('jasper')

    def install(self, spec, prefix):
        process=subprocess.Popen(['./configure', '--prefix=%s' % prefix], stdin=subprocess.PIPE)
        process.communicate(input='1\n')
        # configure("--prefix=%s 1" % prefix)
        subprocess.call(['./compile'])
        subprocess.call(['cp', '-r'] + glob('*') + [prefix])
        # make()
        #make("install")
        print 'done?'
        touch('blah.txt')
