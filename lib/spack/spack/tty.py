##############################################################################
# Copyright (c) 2013, Lawrence Livermore National Security, LLC.
# Produced at the Lawrence Livermore National Laboratory.
#
# This file is part of Spack.
# Written by Todd Gamblin, tgamblin@llnl.gov, All rights reserved.
# LLNL-CODE-647188
#
# For details, see https://scalability-llnl.github.io/spack
# Please also see the LICENSE file for our notice and the LGPL.
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License (as published by
# the Free Software Foundation) version 2.1 dated February 1999.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the IMPLIED WARRANTY OF
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the terms and
# conditions of the GNU General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with this program; if not, write to the Free Software Foundation,
# Inc., 59 Temple Place, Suite 330, Boston, MA 02111-1307 USA
##############################################################################
import sys
import spack
from spack.color import *

indent = "  "

def msg(message, *args):
    cprint("@*b{==>} %s" % cescape(message))
    for arg in args:
        print indent + str(arg)


def info(message, *args, **kwargs):
    format = kwargs.get('format', '*b')
    cprint("@%s{==>} %s" % (format, cescape(str(message))))
    for arg in args:
        print indent + str(arg)


def verbose(message, *args):
    if spack.verbose:
        info(str(message), *args, format='c')


def debug(*args):
    if spack.debug:
        info("Debug: " + str(message), *args, format='*g')


def error(message, *args):
    info("Error: " + str(message), *args, format='*r')


def warn(message, *args):
    info("Warning: " + str(message), *args, format='*Y')


def die(message, *args):
    error(message, *args)
    sys.exit(1)


def pkg(message):
    """Outputs a message with a package icon."""
    import platform
    from version import Version

    mac_ver = platform.mac_ver()[0]
    if mac_ver and Version(mac_ver) >= Version('10.7'):
        print u"\U0001F4E6" + indent,
    else:
        cwrite('@*g{[+]} ')
    print message


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
        ans = raw_input(prompt)
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
