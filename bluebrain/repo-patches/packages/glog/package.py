from spack import *
from spack.pkg.builtin.glog import Glog as BuiltinGlog


class Glog(BuiltinGlog):
    depends_on('cmake@3:', type='build')
