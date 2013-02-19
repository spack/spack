#!/usr/bin/env python
import sys
import os
import subprocess
import argparse

def get_path(name):
    path = os.environ.get(name, "")
    return path.split(":")

# Import spack parameters through the build environment.
spack_lib      = os.environ.get("SPACK_LIB")
spack_prefix   = os.environ.get("SPACK_PREFIX")
spack_deps     = get_path("SPACK_DEPENDENCIES")
spack_env_path = get_path("SPACK_ENV_PATH")
if not spack_lib or spack_deps == None:
    print "%s must be run from spack." % os.path.abspath(sys.argv[0])
    sys.exit(1)

# Figure out what type of operation we're doing
command = os.path.basename(sys.argv[0])

# Grab a minimal set of spack packages
sys.path.append(spack_lib)
from spack.utils import *
from spack.compilation import parse_rpaths
import spack.tty as tty

parser = argparse.ArgumentParser(add_help=False)
parser.add_argument("-I", action='append', default=[], dest='include_path')
parser.add_argument("-L", action='append', default=[], dest='lib_path')
parser.add_argument("-l", action='append', default=[], dest='libs')

options, other_args = parser.parse_known_args()
rpaths, other_args = parse_rpaths(other_args)

if rpaths:
    tty.warn("Spack stripping non-spack rpaths: ", *rpaths)

# Find the actual command the build is trying to run by removing
# Spack's env paths from the path.  We use this later for which()
script_dir = os.path.dirname(os.path.expanduser(__file__))
clean_path = get_path("PATH")
remove_items(clean_path, '.')
for path in spack_env_path:
    remove_items(clean_path, path)

# Add dependence's paths to our compiler flags.
def append_if_dir(path_list, prefix, *dirs):
    full_path = os.path.join(prefix, *dirs)
    if os.path.isdir(full_path):
        path_list.append(full_path)

for prefix in spack_deps:
    append_if_dir(options.include_path, prefix, "include")
    append_if_dir(options.lib_path, prefix, "lib")
    append_if_dir(options.lib_path, prefix, "lib64")

# Add our modified arguments to it.
cmd = which(command, path=clean_path)
arguments  = ['-I%s' % path for path in options.include_path]
arguments += other_args
arguments += ['-L%s' % path for path in options.lib_path]
arguments += ['-l%s' % path for path in options.libs]

spack_rpaths = [spack_prefix] + spack_deps
arguments += ['-Wl,-rpath,%s/lib64' % path for path in spack_rpaths]
arguments += ['-Wl,-rpath,%s/lib' % path for path in spack_rpaths]

# Unset some pesky environment variables
pop_keys(os.environ, "LD_LIBRARY_PATH", "LD_RUN_PATH", "DYLD_LIBRARY_PATH")


sys.stderr.write(" ".join(arguments))

rcode = cmd(*arguments, fail_on_error=False)
sys.exit(rcode)
