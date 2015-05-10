from spack import *
import subprocess
from glob import glob
import os
import fileinput

class WrfWps(Package):
    """Description"""

 #   homepage = "http://www.example.com"
    url      = "http://www2.mmm.ucar.edu/wrf/src/WPSV3.6.1.TAR.gz"

    version('3.6.1') 
    
    depends_on('ben-netcdf-fortran')
    depends_on('ben-netcdf')
    depends_on('jasper')
    depends_on('wrf')
    depends_on('tcsh')

    def install(self, spec, prefix):
        # print os.listdir('../WPS')
        first = True
        for line in fileinput.input("compile", inplace=True):
            if first:
                first = False
                print "#!%s/csh -f" % spec['tcsh'].prefix.bin,
            else:
                print line,
        fileinput.close()
        print os.environ['PATH'] , '\n'
        print os.listdir(os.getcwd())
        symlink(spec['wrf'].prefix, '../WRFV3')
        process=subprocess.Popen(['./configure', '--prefix=%s' % prefix], stdin=subprocess.PIPE)
        process.communicate(input='1\n')
        # configure("--prefix=%s 1" % prefix)
        subprocess.call(['./compile'])
        subprocess.call(['cp', '-r'] + glob('*') + [prefix])
        # make()
        #make("install")
        print 'done?'
        touch('blah.txt')
