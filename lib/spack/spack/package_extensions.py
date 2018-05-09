import os
import shutil
import stat


def write_pkgconfig_wrapper(pkg):
    pkgconf_exe = os.path.join(pkg.prefix.bin, 'pkg-config')
    pkgconf_relocate = os.path.join(pkg.prefix.bin, 'pkg-config.orig')
    shutil.move(pkgconf_exe, pkgconf_relocate)

    script = """#!/bin/sh
if [ "$SPACK_DIRTY" = "1" ]; then
    cpath_val=$CPATH
else
    cpath_val=
fi
CPATH=$cpath_val {0} "$@"
""".format(pkgconf_relocate)
    with open(pkgconf_exe, 'w') as F:
        F.write(script)
    mode = os.stat(pkgconf_exe).st_mode
    os.chmod(pkgconf_exe, mode | stat.S_IEXEC)
