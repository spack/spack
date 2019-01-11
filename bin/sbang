#!/bin/bash
#
# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

#
# `sbang`: Run scripts with long shebang lines.
#
# Many operating systems limit the length of shebang lines, making it
# hard to use interpreters that are deep in the directory hierarchy.
# `sbang` can run such scripts, either as a shebang interpreter, or
# directly on the command line.
#
# Usage
# -----------------------------
# Suppose you have a script, long-shebang.sh, like this:
#
#     1    #!/very/long/path/to/some/interpreter
#     2
#     3    echo "success!"
#
# Invoking this script will result in an error on some OS's.  On
# Linux, you get this:
#
#     $ ./long-shebang.sh
#     -bash: ./long: /very/long/path/to/some/interp: bad interpreter:
#            No such file or directory
#
# On Mac OS X, the system simply assumes the interpreter is the shell
# and tries to run with it, which is likely not what you want.
#
#
# `sbang` on the command line
# -----------------------------
# You can use `sbang` in two ways.  The first is to use it directly,
# from the command line, like this:
#
#     $ sbang ./long-shebang.sh
#     success!
#
#
# `sbang` as the interpreter
# -----------------------------
# You can also use `sbang` *as* the interpreter for your script. Put
# `#!/bin/bash /path/to/sbang` on line 1, and move the original
# shebang to line 2 of the script:
#
#     1    #!/bin/bash /path/to/sbang
#     2    #!/long/path/to/real/interpreter with arguments
#     3
#     4    echo "success!"
#
#     $ ./long-shebang.sh
#     success!
#
# On Linux, you could shorten line 1 to `#!/path/to/sbang`, but other
# operating systems like Mac OS X require the interpreter to be a
# binary, so it's best to use `sbang` as a `bash` argument.
# Obviously, for this to work, `sbang` needs to have a short enough
# path that *it* will run without hitting OS limits.
#
# For Lua, scripts the second line can't start with #!, as # is not
# the comment character in lua (even though lua ignores #! on the
# *first* line of a script).  So, instrument a lua script like this,
# using -- instead of # on the second line:
#
#     1    #!/bin/bash /path/to/sbang
#     2    --!/long/path/to/lua with arguments
#     3
#     4    print "success!"
#
# How it works
# -----------------------------
# `sbang` is a very simple bash script. It looks at the first two
# lines of a script argument and runs the last line starting with
# `#!`, with the script as an argument. It also forwards arguments.
#

# First argument is the script we want to actually run.
script="$1"

# Search the first two lines of script for interpreters.
lines=0
while read line && ((lines < 2)) ; do
    if [[ "$line" = '#!'* ]]; then
        interpreter="${line#\#!}"
    elif [[ "$line" = '//!'*node* ]]; then
        interpreter="${line#//!}"
    elif [[ "$line" = '--!'*lua* ]]; then
        interpreter="${line#--!}"
    fi
    lines=$((lines+1))
done < "$script"
# this is ineeded for scripts with sbang parameter
# like ones in intltool
# #!/<spack-long-path>/perl -w
# this is the interpreter line with all the parameters as a vector
interpreter_v=(${interpreter})
# this is the single interpreter path 
interpreter_f="${interpreter_v[0]}"

# Invoke any interpreter found, or raise an error if none was found.
if [[ -n "$interpreter_f" ]]; then
    if [[ "${interpreter_f##*/}" = "perl" ]]; then
        exec $interpreter_v -x "$@"
    else
        exec $interpreter_v "$@"
    fi
else
    echo "error: sbang found no interpreter in $script"
    exit 1
fi
