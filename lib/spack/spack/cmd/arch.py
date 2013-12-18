import spack
import spack.architecture as architecture

description = "Print the architecture for this machine"

def arch(parser, args):
    configured_sys_type = arch.get_sys_type_from_spack_globals()
    if not configured_sys_type:
        configured_sys_type = "autodetect"
    print "Configured sys_type:             %s" % configured_sys_type
    print "Autodetected default sys_type:   %s" % arch.sys_type()
