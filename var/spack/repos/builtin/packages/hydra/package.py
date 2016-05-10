from spack import *

class Hydra(Package):
    """Hydra is a process management system for starting parallel jobs.
    Hydra is designed to natively work with existing launcher daemons
    (such as ssh, rsh, fork), as well as natively integrate with resource
    management systems (such as slurm, pbs, sge)."""

    homepage = "http://www.mpich.org"
    url      = "http://www.mpich.org/static/downloads/3.2/hydra-3.2.tar.gz"
    list_url = "http://www.mpich.org/static/downloads/"
    list_depth = 2

    version('3.2', '4d670916695bf7e3a869cc336a881b39')


    def install(self, spec, prefix):
        configure('--prefix=%s' % prefix)

        make()
        make("install")
