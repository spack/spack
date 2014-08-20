#!/usr/bin/env python
import sys
if not sys.version_info[:2] >= (2,6):
    sys.exit("Spack requires Python 2.6.  Version was %s." % sys.version_info)

import os
import re
import subprocess
from contextlib import closing

# Import spack parameters through the build environment.
spack_lib = os.environ.get("SPACK_LIB")
if not spack_lib:
    print "Spack compiler must be run from spack!"
    sys.exit(1)

# Grab a minimal set of spack packages
sys.path.append(spack_lib)
from spack.compilation import *
from external import argparse
import llnl.util.tty as tty

spack_prefix        = get_env_var("SPACK_PREFIX")
spack_debug         = get_env_flag("SPACK_DEBUG")
spack_deps          = get_path("SPACK_DEPENDENCIES")
spack_env_path      = get_path("SPACK_ENV_PATH")
spack_debug_log_dir = get_env_var("SPACK_DEBUG_LOG_DIR")
spack_spec          = get_env_var("SPACK_SPEC")

compiler_spec = get_env_var("SPACK_COMPILER_SPEC")
spack_cc  = get_env_var("SPACK_CC",  required=False)
spack_cxx = get_env_var("SPACK_CXX", required=False)
spack_f77 = get_env_var("SPACK_F77", required=False)
spack_fc  = get_env_var("SPACK_FC",  required=False)

# Figure out what type of operation we're doing
command = os.path.basename(sys.argv[0])

cpp, cc, ccld, ld, version_check = range(5)

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


if command in ('cc', 'gcc', 'c89', 'c99', 'clang'):
    command = spack_cc
    language = "C"
elif command in ('c++', 'CC', 'g++', 'clang++'):
    command = spack_cxx
    language = "C++"
elif command in ('f77'):
    command = spack_f77
    language = "Fortran 77"
elif command in ('fc', 'f90', 'f95'):
    command = spack_fc
    language = "Fortran 90"
elif command in ('ld', 'cpp'):
    pass # leave it the same.  TODO: what's the right thing?
else:
    raise Exception("Unknown compiler: %s" % command)

if command is None:
    print "ERROR: Compiler '%s' does not support compiling %s programs." % (
        compiler_spec, language)
    sys.exit(1)

version_args = ['-V', '-v', '--version', '-dumpversion']
if any(arg in sys.argv for arg in version_args):
    mode = version_check

# Parse out the includes, libs, etc. so we can adjust them if need be.
parser = argparse.ArgumentParser(add_help=False)
parser.add_argument("-I", action='append', default=[], dest='include_path')
parser.add_argument("-L", action='append', default=[], dest='lib_path')
parser.add_argument("-l", action='append', default=[], dest='libs')

options, other_args = parser.parse_known_args()
rpaths, other_args = parse_rpaths(other_args)

# Add dependencies' include and lib paths to our compiler flags.
def add_if_dir(path_list, directory, index=None):
    if os.path.isdir(directory):
        if index is None:
            path_list.append(directory)
        else:
            path_list.insert(index, directory)

for dep_dir in spack_deps:
    add_if_dir(options.include_path, os.path.join(dep_dir, "include"))
    add_if_dir(options.lib_path,     os.path.join(dep_dir, "lib"))
    add_if_dir(options.lib_path,     os.path.join(dep_dir, "lib64"))

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
remove_paths = ['.'] + spack_env_path
path = [p for p in get_path("PATH") if p not in remove_paths]
os.environ["PATH"] = ":".join(path)

full_command = [command] + arguments

if spack_debug:
    input_log = os.path.join(spack_debug_log_dir,  'spack-cc-%s.in.log' % spack_spec)
    output_log = os.path.join(spack_debug_log_dir, 'spack-cc-%s.out.log' % spack_spec)
    with closing(open(input_log, 'a')) as log:
        args = [os.path.basename(sys.argv[0])] + sys.argv[1:]
        log.write("%s\n" % " ".join(arg.replace(' ', r'\ ') for arg in args))
    with closing(open(output_log, 'a')) as log:
        log.write("%s\n" % " ".join(full_command))

rcode = subprocess.call(full_command)
sys.exit(rcode)
