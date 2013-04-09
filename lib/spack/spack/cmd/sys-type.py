import spack
import spack.arch as arch

description = "Print the spack sys_type for this machine"

def sys_type(parser, args):
    configured_sys_type = arch.get_sys_type_from_spack_globals()
    if not configured_sys_type:
        configured_sys_type = "autodetect"
    print "Configured sys_type:             %s" % configured_sys_type
    print "Autodetected default sys_type:   %s" % arch.sys_type()
