#!/usr/bin/env python
import sys
import os
import subprocess
import argparse

# reimplement some tty stuff to minimize imports
blue, green, yellow, reset = [
    '\033[1;39m', '\033[1;92m', '\033[4;33m', '\033[0m']

# Import spack parameters through the build environment.
spack_lib      = os.environ.get("SPACK_LIB")
if not spack_lib:
    print "Spack compiler must be run from spack!"
    sys.exit(1)

# Grab a minimal set of spack packages
sys.path.append(spack_lib)
from spack.compilation import *
import spack.tty as tty

spack_prefix   = get_env_var("SPACK_PREFIX")
spack_debug    = get_env_flag("SPACK_DEBUG")
spack_deps     = get_path("SPACK_DEPENDENCIES")
spack_env_path = get_path("SPACK_ENV_PATH")

# Figure out what type of operation we're doing
command = os.path.basename(sys.argv[0])

parser = argparse.ArgumentParser(add_help=False)
parser.add_argument("-I", action='append', default=[], dest='include_path')
parser.add_argument("-L", action='append', default=[], dest='lib_path')
parser.add_argument("-l", action='append', default=[], dest='libs')

options, other_args = parser.parse_known_args()
rpaths, other_args = parse_rpaths(other_args)

if rpaths:
    print "{}Warning{}: Spack stripping non-spack rpaths: ".format(yellow, reset)
    for rp in rpaths: print "  %s" % rp

# Ensure that the delegated command doesn't just call this script again.
clean_path = get_path("PATH")
for item in ['.'] + spack_env_path:
    if item in clean_path:
        clean_path.remove(item)
os.environ["PATH"] = ":".join(clean_path)

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
arguments  = ['-I%s' % path for path in options.include_path]
arguments += other_args
arguments += ['-L%s' % path for path in options.lib_path]
arguments += ['-l%s' % path for path in options.libs]

spack_rpaths = [spack_prefix] + spack_deps
arguments += ['-Wl,-rpath,%s/lib64' % path for path in spack_rpaths]
arguments += ['-Wl,-rpath,%s/lib' % path for path in spack_rpaths]

# Unset some pesky environment variables
for var in ["LD_LIBRARY_PATH", "LD_RUN_PATH", "DYLD_LIBRARY_PATH"]:
    if var in os.environ:
        os.environ.pop(var)

if spack_debug:
    sys.stderr.write("{}==>{} {} {}\n".format(
            green, reset, command, " ".join(arguments)))

rcode = subprocess.call([command] + arguments)
sys.exit(rcode)
