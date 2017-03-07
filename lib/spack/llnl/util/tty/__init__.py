##############################################################################
# Copyright (c) 2013-2016, Lawrence Livermore National Security, LLC.
# Produced at the Lawrence Livermore National Laboratory.
#
# This file is part of Spack.
# Created by Todd Gamblin, tgamblin@llnl.gov, All rights reserved.
# LLNL-CODE-647188
#
# For details, see https://github.com/llnl/spack
# Please also see the LICENSE file for our notice and the LGPL.
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License (as
# published by the Free Software Foundation) version 2.1, February 1999.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the IMPLIED WARRANTY OF
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the terms and
# conditions of the GNU Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public
# License along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA 02111-1307 USA
##############################################################################
import sys
import os
import textwrap
import fcntl
import termios
import struct
import traceback
from six import StringIO

from llnl.util.tty.color import *

_debug   = False
_verbose = False
_stacktrace = False
indent  = "  "


def is_verbose():
    return _verbose


def is_debug():
    return _debug


def is_stacktrace():
    return _stacktrace


def set_debug(flag):
    global _debug
    _debug = flag


def set_verbose(flag):
    global _verbose
    _verbose = flag


def set_stacktrace(flag):
    global _stacktrace
    _stacktrace = flag


def process_stacktrace(countback):
    """Gives file and line frame 'countback' frames from the bottom"""
    st = traceback.extract_stack()
    # Not all entries may be spack files, we have to remove those that aren't.
    file_list = []
    for frame in st:
        # Check that the file is a spack file
        if frame[0].find("/spack") >= 0:
            file_list.append(frame[0])
    # We use commonprefix to find what the spack 'root' directory is.
    root_dir = os.path.commonprefix(file_list)
    root_len = len(root_dir)
    st_idx = len(st) - countback - 1
    st_text = "%s:%i " % (st[st_idx][0][root_len:], st[st_idx][1])
    return st_text


def msg(message, *args, **kwargs):
    newline = kwargs.get('newline', True)
    st_text = ""
    if _stacktrace:
        st_text = process_stacktrace(2)
    if newline:
        cprint("@*b{%s==>} %s" % (st_text, cescape(message)))
    else:
        cwrite("@*b{%s==>} %s" % (st_text, cescape(message)))
    for arg in args:
        print(indent + str(arg))


def info(message, *args, **kwargs):
    format = kwargs.get('format', '*b')
    stream = kwargs.get('stream', sys.stdout)
    wrap   = kwargs.get('wrap', False)
    break_long_words = kwargs.get('break_long_words', False)
    st_countback = kwargs.get('countback', 3)

    st_text = ""
    if _stacktrace:
        st_text = process_stacktrace(st_countback)
    cprint("@%s{%s==>} %s" % (format, st_text, cescape(str(message))),
           stream=stream)
    for arg in args:
        if wrap:
            lines = textwrap.wrap(
                str(arg), initial_indent=indent, subsequent_indent=indent,
                break_long_words=break_long_words)
            for line in lines:
                stream.write(line + '\n')
        else:
            stream.write(indent + str(arg) + '\n')


def verbose(message, *args, **kwargs):
    if _verbose:
        kwargs.setdefault('format', 'c')
        info(message, *args, **kwargs)


def debug(message, *args, **kwargs):
    if _debug:
        kwargs.setdefault('format', 'g')
        kwargs.setdefault('stream', sys.stderr)
        info(message, *args, **kwargs)


def error(message, *args, **kwargs):
    kwargs.setdefault('format', '*r')
    kwargs.setdefault('stream', sys.stderr)
    info("Error: " + str(message), *args, **kwargs)


def warn(message, *args, **kwargs):
    kwargs.setdefault('format', '*Y')
    kwargs.setdefault('stream', sys.stderr)
    info("Warning: " + str(message), *args, **kwargs)


def die(message, *args, **kwargs):
    kwargs.setdefault('countback', 4)
    error(message, *args, **kwargs)
    sys.exit(1)


def get_number(prompt, **kwargs):
    default = kwargs.get('default', None)
    abort = kwargs.get('abort', None)

    if default is not None and abort is not None:
        prompt += ' (default is %s, %s to abort) ' % (default, abort)
    elif default is not None:
        prompt += ' (default is %s) ' % default
    elif abort is not None:
        prompt += ' (%s to abort) ' % abort

    number = None
    while number is None:
        msg(prompt, newline=False)
        ans = raw_input()
        if ans == str(abort):
            return None

        if ans:
            try:
                number = int(ans)
                if number < 1:
                    msg("Please enter a valid number.")
                    number = None
            except ValueError:
                msg("Please enter a valid number.")
        elif default is not None:
            number = default
    return number


def get_yes_or_no(prompt, **kwargs):
    default_value = kwargs.get('default', None)

    if default_value is None:
        prompt += ' [y/n] '
    elif default_value is True:
        prompt += ' [Y/n] '
    elif default_value is False:
        prompt += ' [y/N] '
    else:
        raise ValueError(
            "default for get_yes_no() must be True, False, or None.")

    result = None
    while result is None:
        msg(prompt, newline=False)
        ans = raw_input().lower()
        if not ans:
            result = default_value
            if result is None:
                print("Please enter yes or no.")
        else:
            if ans == 'y' or ans == 'yes':
                result = True
            elif ans == 'n' or ans == 'no':
                result = False
    return result


def hline(label=None, **kwargs):
    """Draw a labeled horizontal line.
       Options:
       char       Char to draw the line with.  Default '-'
       max_width  Maximum width of the line.  Default is 64 chars.
    """
    char      = kwargs.pop('char', '-')
    max_width = kwargs.pop('max_width', 64)
    if kwargs:
        raise TypeError(
            "'%s' is an invalid keyword argument for this function."
            % next(kwargs.iterkeys()))

    rows, cols = terminal_size()
    if not cols:
        cols = max_width
    else:
        cols -= 2
    cols = min(max_width, cols)

    label = str(label)
    prefix = char * 2 + " "
    suffix = " " + (cols - len(prefix) - clen(label)) * char

    out = StringIO()
    out.write(prefix)
    out.write(label)
    out.write(suffix)

    print(out.getvalue())


def terminal_size():
    """Gets the dimensions of the console: (rows, cols)."""
    def ioctl_GWINSZ(fd):
        try:
            rc = struct.unpack('hh', fcntl.ioctl(
                fd, termios.TIOCGWINSZ, '1234'))
        except:
            return
        return rc
    rc = ioctl_GWINSZ(0) or ioctl_GWINSZ(1) or ioctl_GWINSZ(2)
    if not rc:
        try:
            fd = os.open(os.ctermid(), os.O_RDONLY)
            rc = ioctl_GWINSZ(fd)
            os.close(fd)
        except:
            pass
    if not rc:
        rc = (os.environ.get('LINES', 25), os.environ.get('COLUMNS', 80))

    return int(rc[0]), int(rc[1])
