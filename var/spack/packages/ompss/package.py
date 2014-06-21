from spack import *
import os
import glob
import subprocess

# working config lines for ompss 14.06 :
#./mcxx-1.99.2/config.log:	$ ./configure --prefix=/usr/gapps/exmatex/ompss --with-nanox=/usr/gapps/exmatex/ompss --enable-ompss --with-mpi=/opt/mvapich2-intel-shmem-1.7 --enable-tl-openmp-profile --enable-tl-openmp-intel
#./nanox-0.7/config.log:	$ ./configure --prefix=/usr/gapps/exmatex/ompss --with-mcc=/usr/gapps/exmatex/ompss/ --with-hwloc=/usr

class Ompss(Package):
    homepage = "http://pm.bsc.es/"
    url      = "http://pm.bsc.es/sites/default/files/ftp/ompss/releases/ompss-14.06.tar.gz"
    versions  = { '14.06' : '99be5dce74c0d7eea42636d26af47b4181ae2e11' }

    # all dependencies are optional, really
    depends_on("mpi")
    #depends_on("openmp")
    #depends_on("hwloc")

    def install(self, spec, prefix):
        if 'openmpi' in spec:
            mpi = spec['openmpi']
        elif 'mpich' in spec:
            mpi = spec['mpich']
        elif 'mvapich' in spec:
            mpi = spec['mvapich']

        os.chdir(glob.glob('./nanox-*').pop())
        #configure("-prefix=" + prefix + " -with-mcc=" + prefix + " -with-hwloc=" + spec['hwloc'].prefix)
        #configure("-prefix=" + prefix, "-with-mcc=" + prefix)
        subprocess.check_call(["configure", "-prefix=" + prefix, "-with-mcc=" + prefix])
        make()
        make("install")

        os.chdir(glob.glob('../mcxx-*').pop())
        #configure("-prefix=" + prefix + " -with-nanox=" + prefix + " -enable-ompss -with-mpi=" + mpi.prefix)
        #configure("-prefix=" + prefix, "-with-nanox=" + prefix, "-enable-ompss", "-with-mpi=" + mpi.prefix)
        subprocess.check_call(['configure', "-prefix=" + prefix, "-with-nanox=" + prefix, "-enable-ompss", "-with-mpi=" + mpi.prefix])
        make()
        make("install")

