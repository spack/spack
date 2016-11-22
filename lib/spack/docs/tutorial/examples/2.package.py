# flake8: noqa

from spack import *

class Mpileaks(AutotoolsPackage):
    """Tool to detect and report MPI objects like MPI_Requests and MPI_Datatypes"""

    homepage = "https://github.com/hpc/mpileaks"
    url      = "https://github.com/hpc/mpileaks/releases/download/v1.0/mpileaks-1.0.tar.gz"

    version('1.0', '8838c574b39202a57d7c2d68692718aa')

    depends_on('mpi')
    depends_on('adept-utils')
    depends_on('callpath')

    def configure_args(self):
       # FIXME: Add arguments other than --prefix
       # FIXME: If not needed delete the function
       args = []
       return args
