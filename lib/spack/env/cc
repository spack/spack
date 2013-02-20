#!/usr/bin/env python
import sys
import os
import re
import subprocess
import argparse
from contextlib import closing

# Import spack parameters through the build environment.
spack_lib      = os.environ.get("SPACK_LIB")
if not spack_lib:
    print "Spack compiler must be run from spack!"
    sys.exit(1)

# Grab a minimal set of spack packages
sys.path.append(spack_lib)
from spack.compilation import *
import spack.tty as tty

spack_prefix     = get_env_var("SPACK_PREFIX")
spack_build_root = get_env_var("SPACK_BUILD_ROOT")
spack_debug      = get_env_flag("SPACK_DEBUG")
spack_deps       = get_path("SPACK_DEPENDENCIES")
spack_env_path   = get_path("SPACK_ENV_PATH")

# Figure out what type of operation we're doing
command = os.path.basename(sys.argv[0])
cpp, cc, ccld, ld = range(4)
if command == 'cpp':
    mode = cpp
elif command == 'ld':
    mode = ld
elif '-E' in sys.argv:
    mode = cpp
elif '-c' in sys.argv:
    mode = cc
else:
    mode = ccld

# Parse out the includes, libs, etc. so we can adjust them if need be.
parser = argparse.ArgumentParser(add_help=False)
parser.add_argument("-I", action='append', default=[], dest='include_path')
parser.add_argument("-L", action='append', default=[], dest='lib_path')
parser.add_argument("-l", action='append', default=[], dest='libs')

options, other_args = parser.parse_known_args()
rpaths, other_args = parse_rpaths(other_args)

# Add dependencies' include and lib paths to our compiler flags.
def append_if_dir(path_list, *dirs):
    full_path = os.path.join(*dirs)
    if os.path.isdir(full_path):
        path_list.append(full_path)

for dep_dir in spack_deps:
    append_if_dir(options.include_path, dep_dir, "include")
    append_if_dir(options.lib_path,     dep_dir, "lib")
    append_if_dir(options.lib_path,     dep_dir, "lib64")

# Add our modified arguments to it.
arguments  = ['-I%s' % path for path in options.include_path]
arguments += other_args
arguments += ['-L%s' % path for path in options.lib_path]
arguments += ['-l%s' % path for path in options.libs]

# Add rpaths to install dir and its dependencies.  We add both lib and lib64
# here because we don't know which will be created.
rpaths.extend(options.lib_path)
rpaths.append('%s/lib'   % spack_prefix)
rpaths.append('%s/lib64' % spack_prefix)
if mode == ccld:
    arguments += ['-Wl,-rpath,%s' % p for p in rpaths]
elif mode == ld:
    pairs = [('-rpath', '%s' % p) for p in rpaths]
    arguments += [item for sublist in pairs for item in sublist]

# Unset some pesky environment variables
for var in ["LD_LIBRARY_PATH", "LD_RUN_PATH", "DYLD_LIBRARY_PATH"]:
    if var in os.environ:
        os.environ.pop(var)

# Ensure that the delegated command doesn't just call this script again.
clean_path = get_path("PATH")
for item in ['.'] + spack_env_path:
    if item in clean_path:
        clean_path.remove(item)
os.environ["PATH"] = ":".join(clean_path)

full_command = [command] + arguments
if spack_debug:
    input_log = os.path.join(spack_build_root, 'spack_cc_in.log')
    output_log = os.path.join(spack_build_root, 'spack_cc_out.log')
    with closing(open(input_log, 'a')) as log:
        args = [os.path.basename(sys.argv[0])] + sys.argv[1:]
        log.write("%s\n" % " ".join(arg.replace(' ', r'\ ') for arg in args))
    with closing(open(output_log, 'a')) as log:
        log.write("%s\n" % " ".join(full_command))

rcode = subprocess.call(full_command)
sys.exit(rcode)
