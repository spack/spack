from spack import *

class Bbcp(Package):
    """Securely and quickly copy data from source to target"""
    homepage = "http://www.slac.stanford.edu/~abh/bbcp/"

    version('git', git='http://www.slac.stanford.edu/~abh/bbcp/bbcp.git', branch="master")

    def install(self, spec, prefix):
        cd("src")
        make()
        # BBCP wants to build the executable in a directory whose name depends on the system type
        makesname = Executable("../MakeSname")
        bbcp_executable_path = "../bin/%s/bbcp" % makesname(output=str).rstrip("\n")
        destination_path = "%s/bin/" % prefix
        mkdirp(destination_path)
        install(bbcp_executable_path, destination_path)
