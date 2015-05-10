from spack import *
 
class Trinity(Package):
    """Trinity Spack File"""
 
    homepage = "http://www.example.com"
    url      = "http://www.example.com/Trinity-1.0.tar.gz"
 
    version('1.0',git='https://github.com/trinityrnaseq/trinityrnaseq.git')
    depends_on("mpi")
    parallel=False
    def install(self, spec, prefix):
        make()
